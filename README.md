Lambda Substitution... Literally
================================

A toy plugin for Sublime Text 2 that allows you to use nice Unicode `λ` symbols in your code and text.

Functionality
-------------
- Remaps the `\` key so it outputs `λ` characters.
- Press `\` twice for a backslash.
- On saving a file, `λ` characters will be saved as backslashes.
- On opening a file, all backslashes outside quotes will be converted to `λ` characters.

Caveats
-------
- Buffers will always be dirty due to post-save modification.
- You won't be able to save `λ` literals in your text or differentiate them from backslashes.
- Quotes are assumed to be closed when determining which backslashes to convert. This may cause problems when dealing with a legitimate but uneven number of quotes, such as when working with regexes (see this very plugin's source file for an example).

Why...?
-------
- To get my hands dirty with the Sublime Text API.
- To make writing Haskell code more fun :D

Usage
-----
- Call up the Command Palette and toggle it on or off.
- Most of its functionality is passive, so you should be able to start using it right away.

Todo
----
- More robust ways of performing substitutions, such that more caveats are eliminated.
- Differentiate `λ` characters and backslashes source-wise.
- Find some way to allow `λ` literals (for example by not replacing `λ` characters inside quotes).