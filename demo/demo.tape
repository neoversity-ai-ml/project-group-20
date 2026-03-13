Output demo/demo.gif

Set Padding 10
Set TypingSpeed 50ms

Hide
Type "rm addressbook.pkl"
Enter
Type "clear"
Enter
Type "uv run python -m run"
Enter
ScrollUp 30
Show

Sleep 5s
ScrollDown@100ms 15
Sleep 2s

Type "hello"
Enter
Sleep 1s

Type "add Tetjana 4445556666"
Enter
Sleep 0.5s
Type "add-birthday Tetjana 05.05.1992"
Enter
Sleep 0.5s
Type "add-email Tetjana tetjana@example.com"
Enter
Sleep 0.5s
Type "add-address Tetjana 202 Bug Boulevard, QA Town"
Enter
Sleep 0.5s

Type "add Serhii 1112223333"
Enter
Type "add-birthday Serhii 10.10.1990"
Enter
Type "add-email Serhii serhii@example.com"
Enter
Type "add-address Serhii 101 Code Lane, Dev City"
Enter

Type "add Viktoriia 7778889999"
Enter
Type "add-birthday Viktoriia 01.01.1995"
Enter
Type "add-email Viktoriia vika@example.com"
Enter
Type "add-address Viktoriia 303 Feature Street, Prod Village"
Enter

Type "add Ihor 1231231234"
Enter
Type "add-birthday Ihor 07.07.1988"
Enter
Type "add-email Ihor ihor@example.com"
Enter
Type "add-address Ihor 404 Error Avenue, Debug District"
Enter

# Search for different fields
Type "search Tetjana"
Enter
Sleep 2s

Type "search 888"
Enter
Sleep 2s

Type "search Avenue"
Enter
Sleep 0.1s

Type "search @example.com"
Enter
Sleep 0.1s

# Try a few fuzzy command matches
Type "  ADD-BIRTHDAY  Ihor 08.08.1988"
Enter
Sleep 0.1s

Type "shw-birthday Ihor"
Enter
Sleep 1s

# Show errored commands
Type "add-birthday NonExistentUser 01.01.2000"
Enter
Sleep 0.1s

Type "add InvalidNumber 123"
Enter
Sleep 0.1s

Type "all"
Enter
Sleep 1s

Type "exit"
Enter
Sleep 5s
