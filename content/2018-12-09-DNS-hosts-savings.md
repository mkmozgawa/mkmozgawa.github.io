Title: On saving time and money with /etc/hosts
Date: 2018-12-09 20:00
Modified: 2018-12-09 20:00
Category: Linux
Tags: linux, lifehacks
Slug: DNS-hosts-savings
Authors: Magda Mozgawa
Summary: On saving time and money with /etc/hosts

Recently whenever I'm bored, tired and with just 20 minutes to spare (bored enough so I can't go to sleep early but too tired to do anything productive, and turning on the console for _just 20 minutes_ never works) I got onto the habit of browsing clothes, cosmetics, etc. Maybe I need to fill in some void, or maybe I've been succumbing again to the pressure of looking _presentable_ when going to the office (after several months of remote work spent in some jeans and nondescript t-shirts). Either way, there's clearly a pattern here.

So I gathered the websites I've been using too frequently for no good reason, and added them to ```/etc/hosts```. After a while, I decided to impose that ban on some other sites that seem to bring no value to me. Currently the selection is as follows:

```
# Block super stupid sites I don't want to waste my time on
0.0.0.0 www.reserved.com
0.0.0.0 reserved.com
0.0.0.0 www.housebrand.com
0.0.0.0 housebrand.com
0.0.0.0 www.massimodutti.com
0.0.0.0 massimodutti.com
0.0.0.0 www.cropp.com
0.0.0.0 cropp.com
0.0.0.0 www.wolczanka.pl
0.0.0.0 wolczanka.pl

0.0.0.0 twitter.com
0.0.0.0 www.twitter.com
0.0.0.0 instagram.com
0.0.0.0 www.instagram.com
```

I don't even have accounts on twitter and instagram anymore so why was I browsing them? Muscle memory, I think.

Remember to restart the browser (and flush the dns beforehand, preferably) after each change. On Ubuntu 18.04, it's possible to flush dns with ```sudo systemd-resolve --flush-caches```.

Now what will I do with all that extra time? Perhaps I should order more books :)
