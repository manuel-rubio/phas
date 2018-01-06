PHAS
====

PHP Application Server (PHAS) is a system to write dynamically the code in production with a version control.

**DISCLAIMER** This system was a proof-of-concept and is not finalized. There are a lot of improvements to be performed and it's not recommeded to use in a production system.

The system is based in different elements:

- **lib** (and **htdocs**) is the place where PHP code lives.
- **phasweb** is a Django interface to handle the code.

The code should be wrote in **JavaScript** in the web interface. The system uses *spidermonkey* as JavaScript interpreter on top of PHP.

The main idea was keep publish as many low level components in PHP interfacing to JavaScript as possible and let to the users perform the modifications on-the-fly. But there are a lot of changes to perform:

- Unify the base language (use or only Python or only PHP for the system and web interface)
- Use version control for the whole group of APIs not only based on calls or use specific tags or versions.

If you want to collaborate, make a fork, open an issue and/or send a pull-request.

Enjoy!

