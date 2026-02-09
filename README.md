# STIG_API
I'm constantly having to answer questions about STIGs. Sometimes, when questions are presented or if there is an issue I'm just given the Group ID number. In response, I have made a few Pthon tools to help with these. This is the latest iteration and is a continued work in progress. I have converted one of my tools (or at least started) to this API. The intent is to allow for implementation as needed/desired. I will continue working on this as I have time.

## Needed software/tools
For full API use, you will need to have Ollama installed. There are a couple of API calls used that will call on ollama for AI assistance (answering questions and analyzing STIG output). Model evaluations will be done eventually.
To use this tool, STIGs will need to be downloaded and unzipped. Adjust the configuration.py file with the file locations as well.

###Future Plans
1. Error handling - right now there isn't much in that regard
2. Checking for AI configuration, if not in place it will handle that gracefully
3. Developing some kind of GUI to use the API as well (for those who don't want to do it)
4. Add in additional functionality for the API and supporting scripts to help.