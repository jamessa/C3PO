#Hassle Free Localization

After [all](https://github.com/jamessa/C3PO/blob/master/Introduction.md) these try-and-error, here's my new requirement:

1. Fully automatic and reflect to current code (because we, developers, are lazy)
2. Only ONE set of XIB/NIB is used.
3. Ease of localization

The flow becomes 

1. `genstrings` to make master `Localization.strings`
2. `ibtool` to extract localizable values
3.  merge 1 and 2 with up-to-date localization

C3PO is dedicated to automate this flow. All you need to do is meeting following requirements

##Create a new build phase

	find ${SRCROOT} -name "Localizable.strings" -print | xargs -I {} echo "iconv -f UTF-8 -t UTF-16 =(cat {})> {}"  | zsh
	python ${SRCROOT}/externals/C3PO/localize.py
	find ${SRCROOT} -name "Localizable.strings" -print | xargs -I {} echo "iconv -f UTF-16 -t UTF-8 =(cat {})> {}"  | zsh


##Use NSLocalizedString for all UI strings

    myLabel.text = NSLocalizedString(@"MY_TEXT", nil);

##Use WIDE_CASE or CamelCase in Interface Builder

	<string key="IBUIText">MY_TEXT</string>

or

	<string key="IBUIText">MyTest</string>

##Add following lines to your controller

	- (void) viewDidLoad {
		for (UILabel *aLabel in self.interfaceLabels) {
		aLabel.text = NSLocalizedString(aLabel.text, @"C3PO Localized");
	}

##Your localization string is ready to go

	% find . -name "Localizable.strings"
	./en.lproj/Localizable.strings
	./zh-Hant.lproj/Localizable.strings

Time to take your app to the world. @jamex