#Netball Live addon for Kodi

## This add-on supports the free Live Pass offer from eligible Telstra customers. In-app subscriptions through the App Store/Google Play are NOT supported.

##Requirements

Kodi v17 is the minimum recommended version. If you are having SSL errors, upgrading should solve them. On some platforms earlier version will work fine.

You will need a Telstra ID account with an eligble service attached to use this add-on. Most Telstra Mobile customers are eligble for a free subscription with their plan. Please see their [website](https://www.telstra.com.au/tv-movies-music/sports-offer) for details.

##How to install

Netball Live is available from the Catch Up TV AU repository located [here](https://github.com/xbmc-catchuptv-au/repo). Head on over and follow the instructions to install the repo, then install the add-on. 

##Settings

You will need to enter your Telstra ID username and password to view videos.

The plugin has two replay streaming modes which can be set in the add-on's settings - Apple's http live streaming (HLS) and Adobe's http dynamic streaming (HDS). HLS has a lower maximum quality, HDS is higher. The trade off is that you can seek freely through the video with HLS whereas HDS you can't. Pausing seems to be fine though, at least for short periods of time. For live videos only HLS is available in this add-on, which doesn't matter as the live HDS stream offers the same bitrates anyway.

The live streaming bitrates reflect an average bitrate only, you should ideally have twice the bandwidth available to ensure buffer free viewing.

##Issues

Please let me know of any errors by opening an [issue](https://github.com/glennguy/plugin.video.netball-live/issues) ticket. It would be great if you could attach a Kodi debug log file as well.
