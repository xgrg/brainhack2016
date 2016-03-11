.. image:: https://circleci.com/gh/xgrg/kandu/tree/master.svg?style=shield&circle-token=:circle-token
   :target: https://circleci.com/gh/xgrg/kandu/tree/master

# Kandu

Kandu wants to help with the complex file trees, that make the data impossible to control. It provides a simple web interface for three types of jobs:

  - building regular expressions out of a few clicks
  - checking how these expressions match the filepaths in a given repository
  - perform a full check over a repository

### Version
pre-alpha 1.0

### Usage

Kandu runs a Python web server ([Tornado]) in order to give access to the interface on http://localhost:8888 (default port). Having an Anaconda distribution is a simple way to get operational.

```sh
$ pip install kandu
$ kandu_server --repository /path/to/repo --hierarchy /path/to/output.json
```
Then open a browser at http://localhost:8888.



![alt tag](http://raw.githubusercontent.com/xgrg/kandu/master/doc/screenshot.png)

   [Anaconda]: <https://www.continuum.io/downloads>
   [Tornado]: <http://www.tornadoweb.org/en/stable/>
   [git-repo-url]: <http://daringfireball.net>
   [@thomasfuchs]: <http://twitter.com/thomasfuchs>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [marked]: <https://github.com/chjj/marked>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [keymaster.js]: <https://github.com/madrobby/keymaster>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]:  <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>


