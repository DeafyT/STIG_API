backup_stig_location="/Users/Shared/Supporting_Docs/STIGs/Backup/"
current_stig_location="/Users/Shared/Supporting_Docs/STIGs/Current/"
stig_zip_location="/Users/Shared/Supporting_Docs/STIG_ZIP/"
stig_unzipped_location="/Users/Shared/Supporting_Docs/STIG_ZIP/Unzipped/"

if [[ $EUID -ne 0 ]]; then
    echo "This script needs to run with sudo privileges for the file movement."
    exit 1
fi

# Clear Backup and move current STIGs to backup
rm $backup_stig_location*
mv $current_stig_location* $backup_stig_location

#Get the file name
file=`ls -l ~/Downloads | grep U_S | awk '{print $NF}'`

#Move file to the STIG_ZIP folder
cp ~/Downloads/$file $stig_zip_location

#unzip the folder, remove the pdf files
echo "Unzipping the files and moving the STIG lists to the appropriate folder"
unzip -qq "$stig_zip_location$file" -d $stig_zip_location
rm $stig_zip_location*.pdf
rm "$stig_zip_location$file"

#Iterate through each zip file and unzip it to the unzipped directory
for file in $stig_zip_location*; do
    if [ -f "$file" ]; then
        unzip -qq -o $file -d $stig_unzipped_location
        rm $file
    fi
done

#Iterate through each directory in the unzipped directory and move the .xml files to the original folder
echo "Cleaning up"
mv $stig_unzipped_location*/*.xml $current_stig_location
rm -r $stig_unzipped_location*

echo "Done!"