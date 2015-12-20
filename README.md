# cwpd

Crude Wordpress Plugin Detector is a very basic WP plugin detector. It searches for the readme.txt file which is present in most WP plugins and that is rarely deleted by webmasters.

#How to use it

First of all you need to create the plugin list. You can do this by using listmaker.py which will create a list of the 1000 most popular plugins in the format used by cwpd. You can find more plugins by modifiying the script so that it checks more than the first 50 pages from the popular WordPress plugins list

Then you can use cwpd.py to scan for all of these plugins:

Usage: cwpd.py -w [wp-content folder] -t [number of threads] [target]

The wp-content folder by default is named 'wp-content' and can be ommited. By default 8 threads will be started but this also can be modified.

You'll also need to download a user agent list (http://techpatterns.com/downloads/firefox/useragentswitcher.xml) and rename it to useragents.xml.
