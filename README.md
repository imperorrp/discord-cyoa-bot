# Discord-CYOA-Bot

Welcome to *DCYOAB* (Until I decide upon an actual bot name 👍).
A python-based Discord bot for playing custom-built text adventures on Discord channels! 

#### What is this?
Inspired by the popular choose-your-own-adventure (CYOA) stories (and the myriad others like it, like Give Yourself Goosebumps, so many video games and now a few on-screen movies/series- Black Mirror's Bandersnatch and Minecraft: Story Mode), where *you*, the reader/player/viewer, are given a prompt and some options and you decide what to do next. 

With this project, you can create your own interactive adventures on Google Sheets. People can then select and play them on Discord. 

#### Who this is for:
If you run a Discord server and love bots that add to the community gamification experience, this is for you. Writers/game designers might find this cool too, maybe as a medium to get to Discord users?

#### Roadmap/Contributing
Lots of potential work remaining on this! 
Some examples:
- Privacy: Adventures added to the bot are available to the bot's users on *any* Discord server. This could be changed.
- Image support: Image support (currently plaintext only) to make adventures more flavorful.
- Add end conditions: Wrap ups for the story, dead-ends and the like with no more options.
- Other features, like a stats(?) section 

I'll be working on this now and then, adding features and making edits. Feel free to make pull requests or reach out to me anytime, and contributors are always welcome!

Currently hosting this locally, but I'll set up a main instance on a server soon. Dedicated Discord server for support/dev possibly in the works too- stay tuned!

## Demo/Commands
Some bot commands and basic usage:
#### >about
![About command embed](screenshots/about.png)
#### >help
![Help command embed](screenshots/help.png)
#### >adventures 
![Adventures command embed](screenshots/adventures.png)
#### >start 2
![2nd adventure embed page 1](screenshots/start-2-1.png)

If you *Go left* ->

![2nd adventure embed page 2](screenshots/start-2-2.png)

If you *Go right*->

![2nd adventure embed page 3](screenshots/start-2-3.png)

If you *...to page 4*->

![2nd adventure embed page 4](screenshots/start-2-4.png)

The embed updates (edits itself) when you pick options by hitting the buttons. 

## Deployment

For deploying locally:

Download the required dependencies (currently just the gspread and discord.py APIs)
```
pip install -r requirements. txt
```
Create a new [Discord application](https://discord.com/developers/docs/getting-started), grab your bot token and put it in token.txt.

You'll also have to create a [google cloud service account](https://cloud.google.com/apis/docs/overview) for the bot. You'll get a JSON like so -put it in the project folder:
```
{
  "type": "service_account",
  "project_id": "discord-cyoa-bot",
  "private_key_id": "REDACTED",
  "private_key": "-----BEGIN PRIVATE KEY-----\nREDACTED\n-----END PRIVATE KEY-----\n",
  "client_email": "-----------.iam.gserviceaccount.com",
  "client_id": "REDACTED",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/-----------.iam.gserviceaccount.com"
}

```

Finally, run main.py and try out the commands on Discord.
```
python main.py 
```
