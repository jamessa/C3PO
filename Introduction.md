#Hassle Free Localization

##Apple's way - NSLocalizedString()

[In international programming topic](http://developer.apple.com/library/ios/#documentation/MacOSX/Conceptual/BPInternational/Articles/LocalizingInterfaces.html#//apple_ref/doc/uid/20002138-BBCBFFDF), Apple set up is formal way to localization process.

Use genstrings and ibtool

	ibtool --generate-strings-file MainMenu.strings en.lproj/MainMenu.nib

After localization

	// The translated strings are in the de.lproj directory
	//  with the same name as the original file.
	ibtool --strings-file de.lproj/MainMenu.strings --write de.lproj/MainMenu.nib en.lproj/MainMenu.nib

##Matt Gallagher (aka CocoaWithLove)

[User interface strings in Cocoa](http://cocoawithlove.com/2011/04/user-interface-strings-in-cocoa.html)

	find -E . -iregex '.*\.(m|h|mm)$' -print0 | xargs -0 genstrings -a -o Resources/en.lproj
	
Localize XIB

	for file in *.xib; do
	    ibtool --export-strings-file "$file".strings "$file"
	done

	for file in *.xib.strings; do
	    basename=`basename "$file" .strings`
	    ibtool --strings-file "$file" --write "$basename" "../en.lproj/$basename"
	done

## Wil Shipley

Mentioned in [Lost in Translation](http://blog.wilshipley.com/2009_10_01_archive.html)

Problem 1: Localizers Can’t Effectively Localize Images  
Problem 2: Localizers Can’t Effectively Localize XIBs  
Problem 3: Localizers Can’t Localize from Only Your App  
Problem 4: You Have to Maintain Multiple Copies of Each Localized Resource  

#Requirement for continuous localization

Here're my "musts" for localization:

1. fully automatic and reflect to current code (because we, developers, are lazy)
2. Follow Apple's guideline

#Don't listen, just see what they do.

Let's check /application

	% find . -name "*.nib"
	./Compass.app/MainWindow.nib
	./FieldTest.app/FieldTestSaveViewController.nib

	% find . -name "*.strings"
	./AppStore.app/English.lproj/InfoPlist.strings
	./AppStore.app/English.lproj/Localizable.strings
	./Nike.app/English.lproj/InfoPlist.strings
	./Nike.app/English.lproj/Localizable.strings

	./Preferences.app/English.lproj/5.0~fmf.strings
	./Preferences.app/English.lproj/Brightness.strings
	./Preferences.app/English.lproj/Date & Time.strings
	./Preferences.app/English.lproj/General-Simulator.strings
	./Preferences.app/English.lproj/General~iphone.strings
	./Preferences.app/English.lproj/Home Button.strings
	./Preferences.app/English.lproj/InfoPlist.strings
	./Preferences.app/English.lproj/Localizable~iphone.strings
	./Preferences.app/English.lproj/Location Services.strings
	./Preferences.app/English.lproj/MailNotificationsSettings.strings
	./Preferences.app/English.lproj/MessagesNotificationsSettings.strings
	./Preferences.app/English.lproj/Network.strings
	./Preferences.app/English.lproj/Passcode Lock~iphone.strings
	./Preferences.app/English.lproj/Reset~iphone.strings
	./Preferences.app/English.lproj/Restrictions~iphone.strings
	./Preferences.app/English.lproj/Search Results.strings
	./Preferences.app/English.lproj/Settings~iphone.strings
	./Preferences.app/English.lproj/Software Update.strings
	./Preferences.app/English.lproj/Sounds~iphone.strings
	./Preferences.app/English.lproj/TV-Out.strings
	./Preferences.app/English.lproj/Volume Limit.strings
	./Preferences.app/English.lproj/WYWAAppDetail~iphone.strings

	./Reminders.app/English.lproj/InfoPlist.strings
	./Reminders.app/English.lproj/Localizable.strings

	./Setup.app/English.lproj/AssistantOptIn.strings
	./Setup.app/English.lproj/InfoPlist.strings
	./Setup.app/English.lproj/Localizable.strings
	./Setup.app/English.lproj/RestoreFromBackup.strings


#Setup.app (old standard)

% ls Setup.app/English.lproj

	AssistantOptIn.strings    
	InfoPlist.strings         
	Localizable.strings       
	RestoreFromBackup.strings

% PlistBuddy -c "print" Setup.app/English.lproj/Localizable.strings

	Dict {
	    FIND_MY_IPHONE_NAME_IPHONE = Find My iPhone
	    CANT_CREATE_APPLEID_TITLE = Can't Create Apple ID
	    WHAT_IS_APPLE_ID_FMIP_IPHONE = Use Find My iPhone to locate your iPhone on a map, play a sound, or display a message.
	    WHAT_IS_APPLE_ID_NO_FACETIME = Communicate with iMessage.
	    ABOUT_LOCATION_SERVICES_WEATHER = Weather
	    ICLOUD_BACKUP_EXPLANATION_WIFI_IPAD = Use iCloud to back up your iPad daily over Wi-Fi.
	    WHAT_IS_CASTLE_BACKUP_DESCRIPTION_WLAN_IPAD = iCloud automatically backs up your iPad daily over WLAN when it's connected to a power source.  Purchased music, apps, and books do not count against your 5GB of free iCloud storage.
	    WLAN_SETTINGS = WLAN Settings
	    FIND_MY_IPHONE_BLURB_IPOD = If you misplace your iPod touch, Find My
	iPod touch can help you locate it on a map,
	play a sound, or display a message.
	   	… total 505 lines …
	}

% PlistBuddy -c "print" Setup.app/zh_TW.lproj/Localizable.strings | head

	Dict {
	    HAS_STORE_ACCOUNT_SKIP_APPLEID_ALERT_BODY = 必須有 Apple ID 才能使用 iCloud 和其他服務。建立 Apple ID 不但完全免費，而且十分簡單。
	    CANT_CREATE_APPLEID_TITLE = 不要建立 Apple ID
	    WHAT_IS_APPLE_ID_FMIP_IPHONE = 使用“尋找我的 iPhone”來協助您在地圖上尋找 iPhone、播放提示聲或顯示訊息。
	    WHAT_IS_APPLE_ID_NO_FACETIME = 使用 iMessage 通訊。
	    ABOUT_LOCATION_SERVICES_WEATHER = 天氣
	    ICLOUD_BACKUP_EXPLANATION_WIFI_IPAD = 使用 iCloud 來透過 Wi-Fi 每天備份 iPad。
	    WHAT_IS_CASTLE_BACKUP_DESCRIPTION_WLAN_IPAD = iCloud 會在 iPad 連接電源時每天透過 WLAN 自動進行備份。購買的音樂、應用程式和書籍不會算在免費 5 GB 的 iCloud 儲存空間裡。
	    WLAN_SETTINGS = WLAN 設定
	    FIND_MY_IPHONE_BLURB_IPOD = 若遺失 iPod touch，

% PlistBuddy -c "print" Setup.app/zh_TW.lproj/AssistantOptIn.strings | head 

	Dict {
	    USE_ASSISTANT = 使用 Siri
	    WHAT_IS_SIRI_MESSAGES = 傳送和回應簡訊與電子郵件
	    WHAT_IS_SIRI_WEB = 搜尋網頁
	    WHAT_IS_SIRI_TITLE = Siri
	    WHAT_IS_SIRI_DICTATION = 聽寫文字
	    WHAT_IS_SIRI_DESCRIPTION = Siri 讓您使用語音與 iPhone 互動和使用 iPhone 的許多功能。Siri 可以理解您的語音內容和意思，因此，您可以自然流暢的說出指令，要求 Siri 執行某項作業。Siri 同時知道您的許多資訊，包含您的所在位置、聯絡資訊、聯絡人與您本人的親屬關係等，以便提供智慧型個人助理服務。
	    WHAT_IS_SIRI = 什麼是 Siri？

#FindMyFriends (new standard)

% ls English.lproj

	CreateAccountLocalizable.strings
	DeprecatedAppView-iPad.nib
	DeprecatedAppView.nib
	InfoPlist.strings
	Localizable.strings
	Login-iPad.nib
	Login.nib
	MainWindow-iPad.nib
	MainWindow.nib
	Map.nib

% ls -l English.lproj | awk '{ print $5 "\t" $9 }'
	
	12572	CreateAccountLocalizable.strings
	3174	DeprecatedAppView-iPad.nib
	2763	DeprecatedAppView.nib
	81		InfoPlist.strings
	20739	Localizable.strings
	7637	Login-iPad.nib
	7275	Login.nib
	1933	MainWindow-iPad.nib
	1933	MainWindow.nib
	2280	Map.nib
	4020	NewAccountEmailVerify-iPad.nib
	3513	NewAccountEmailVerify.nib
	1377	NoAccount.nib
	1938	VerifyingEmail-iPad.nib
	1906	VerifyingEmail.nib

% PlistBuddy -c "print" English.lproj/Localizable.strings | head

	Dict {
	    STATE_ONLY_LABEL = %@
	    TEMPORARY_EVENT_REMOVE_FRIEND_AND_LEAVE_MESSAGE = To remove %@, you must also leave “%@” and stop sharing locations with all other invitees.
	    ACCESSIBILITY_SWITCH_ON = On
	    TEMPORARY_EVENT_MESSAGE_NOT_AVAILABLE_MESSAGE = To send a message, turn on iMessage in settings.
	    INVALID_INVITATION_MESSAGE = This invitation is no longer valid.
	    SIGNIN_WITH_RESTRICTIONS_MESSAGE = Disable Restrictions in Settings to sign in to Find My Friends.
	    LOCATING_LABEL = Locating…
	    ACCOUNT_NOTIFICATIONS = Notifications
	    ACCESSIBILITY_HIDE_KEYBOARD_BUTTON = Hide keyboard

#Use ibtool at caution

To relief our localizer's effort, I tried to use ibtool to extract localizable values just like what "genstrings" did. Here's what I did.
 
	ibtool --export-strings-file MyViewController.xib.strings MyViewController.xib
 
work on MyViewController.xib.strings in my localized folder
	
	ibtool --strings-file MyViewController.xib.strings --write MyViewController.xib ../en.lproj/MyViewController.xib
 
But the end result has serious issues, "+" is produced by ibtool, "-" is created in Xcode 4.2.1
 
	<string key="IBDocument.SystemVersion">11C74</string>
	+ <string key="IBDocument.InterfaceBuilderVersion">214</string>
	- <string key="IBDocument.InterfaceBuilderVersion">1938</string>
	<string key="IBDocument.AppKitVersion">1138.23</string>
	<string key="IBDocument.HIToolboxVersion">567.00</string>
	<object class="NSMutableDictionary" key="IBDocument.PluginVersions">
	<string key="NS.key.0">com.apple.InterfaceBuilder.IBCocoaTouchPlugin</string>
	+ <string key="NS.object.0">1145</string>
	- <string key="NS.object.0">933</string>
	 
	...skip...
	 
	<object class="IBUIView" id="191373211">
	+ <nil key="NSNextResponder"/>
	- <reference key="NSNextResponder"/>

#My final solution

After all these try-and-error, here's my new requirement:

1. Fully automatic and reflect to current code (because we, developers, are lazy)
2. Only ONE set of XIB/NIB is used.
3. Ease of localization

The flow becomes 

1. `genstrings` to make master `Localization.strings`
2. `ibtool` to extract localizable values
3.  merge 1 and 2 with up-to-date localization

Problem 1, the format of `ibtool` extracted format is **different** from `genstrings`

	% head en.lproj/Localizable.strings
	/* Action title for discarding a draft */
	"WAActionDiscard" = "Discard";

	% head en.lproj/WAStationDiscoveryFeedbackViewController.xib.strings.new 
	/* Class = "IBUILabel"; text = "WAErrorNoStationFoundTitle"; ObjectID = "3"; */
	"3.text" = "WAErrorNoStationFoundTitle";

Problem 2, both `genstrings` and `ibtool` uses UTF-16 while most diff tool and `git` doesn't treat it correctly.

In my dict, `s/problem/opportunity/i`

Put this into your build phase

	cd ${SRCROOT}/wammer
	find . -name "Localizable.strings" -print | xargs -I {} echo "iconv -f UTF-8 -t UTF-16 =(cat {})> {}"  | zsh
	python ${SRCROOT}/scripts/localize.py
	find . -name "Localizable.strings" -print | xargs -I {} echo "iconv -f UTF-16 -t UTF-8 =(cat {})> {}"  | zsh
