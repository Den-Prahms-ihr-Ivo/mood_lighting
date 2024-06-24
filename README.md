# mood_lighting

## Was habe ich alles gemacht?

### MPD

To add the InnoMaker RPI HIFI DAC hat option to the Raspberry Pi you will need to add a line of text to a configuration file.

Use the following command to open the config.txt file

`sudo nano /boot/firmware/config.txt`

Scroll down to the bottom of that file and add the following text. Make sure it’s pasted exactly as you see it in the screenshot:

Beneath `[all]`
`dtoverlay=allo-boss-dac-pcm512x-audio`

With the DAC hat attached and enabled we’ll just need to find the device number. Check the device number with the following command:

aplay -l

Hit ENTER

This should show you an initial list of devices. For the InnoMaker RPI HIFI DAC you’ll want to look for the BossDAC listing.

NOTE: sometimes this command returns an error instead of a list of devices. I’m not sure why, but if you see an Invalid argument error that suggests removing or fixing ALSA, go ahead and remove it with this command:

rm ~/.asoundrc

If you are asked to confirm the deletion, type yes

Hit ENTER

Then run the following command in Terminal:

cat /proc/asound/cards

Hit ENTER

This will pretty much just confirm the device number of the DAC. You can see in the screenshot that the device number in my case is 3

Find the output device number for your DAC

Set the device as the default soundcard
Now we’ll sent the device number we found as the default soundcard, which should automatically select the DAC as our output device each time you launch the Raspberry Pi.

Use the following command to create and open the sound config file:

sudo nano /etc/asound.conf

Hit Enter

Now, paste the following code block at the bottom of the file:

pcm.!default { type hw card 3 } ctl.!default { type hw card 3 }

Remember to replace the card number with the device number you found in a previous step.

With that new line added, hit the following key command to Write Out and save the file:

Control + O

Hit ENTER

Then exit the config file with the following key command:

Control + X

This is a good time to reboot the Raspberry Pi with the following command:

sudo reboot

Hit Enter

Access the Raspberry Pi config file to change the default audio settings
Now you’ll set the newly added DAC as your default audio output in the Raspberry Pi configuration menu.

Use the following command to open the Raspberry Pi configuration UI:

sudo raspi-config

Hit ENTER

Select System Options → Audio

Select BossDAC from the output list, then select Ok

Important: The device number in the audio output settings should match the device you set as the default soundcard. If it doesn’t, reboot the Raspberry Pi again and re-check sudo raspi-config

### MPD

https://linuxaudiofoundation.org/musiclounge-configure-mpd/

## CURRENT TODOs

- Pin High and Low Kram testen
- MPD Testen
  - Hier besonders das Time Out und die eigentlich Funktion.
  - Notieren der Steps, die ich zum zum Laufen bekommen eingegangen bin notieren
  - In wie weit klappt das mit dem Display?
- Schaltung für Peripherie testen und entwickeln.
- Code in der Gänze auf dem Raspberry testen.
