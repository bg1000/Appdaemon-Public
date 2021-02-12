#  Appdaemon Apps

These are a few of my appdaemon apps that I have cleaned up a bit and written a little documention for.  They are here for people to use, get ideas from or modify for your own use.  My intent is to add to this over time. I am more than willing to colaborate on any of this.  If you run into a problem you are more than welcome to open an issue.  If you have made an improvement and want to share it I open to discussing a pull request. You can also reach me on discord or the home assistant community forums under the same username (bg1000).

# App List

What follows is a list of the apps in this repo with a link to the readme for each app.


| App           | Dependencies  | Description                                            |
| ----------------|---------------|:-------------------------------------------------------|
| [app_messenger](/app_messenger/readme.md)  | None | Centralized notification for android phones.|
| [auto_light](/auto_light)/readme.md      | None      |  Motion light on steroids.|
| [battery_minder](/battery_minder/readme.md) |   app_messenger   |    Set it and forget way to manage batteries.  |
| [cover_tag](/cover_tag/readme.md) |None |Open or close a cover when an NFC tag is scanned. |
| [goodnight](/goodnight/readme.md) | app_messenger | Makes sure the house is ready for bed when an NFC tag is scanned.

# How to use

You are welcome to clone the whole repo of course.  In fact if you clone the repo somewhere under your apps directory appdaemon will try to start the apps for your automatically.  Obvioulsy you will have to change the yaml to meet your needs.  I suspect it is more likely that someone will want one app or even a part of one app.  Each app has it's own yaml file so they are pretty portable.  You can simply use curl or wget to download the .py and .yaml file to your desired location.  Some of the apps are dependant on app_messenger so you'll need to decide if you want to use it or modify the app to handle messaging differently.
