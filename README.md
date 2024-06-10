Article: <a href='https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/02_newapp.html' >A New Application</a>
<br>

1.Using scaffold<br>
This is the command of scaffold for creating Apps.

```
python path-of-oddo-bin/odoo-bin scaffold test_scaffold_module 2.Chapter-2:A-New-Application
```
Now, you can now able to activate.

2.Without scaffold<br>
Create the following folders and files.<br>

     2.Chapter-2:A-New-Application/<br>
     ├── estate<br>
     │   ├── __init__.py<br>
     │   ├── __manifest__.py<br>
     │   ├── models<br>
     │   │   └── __init__.py<br>
     │   └── __pycache__<br>
     │       └── __init__.cpython-310.pyc<br>
     ├── README.md <br>
<img src='https://www.odoo.com/documentation/17.0/_images/app_in_list.png'>
<br>
real_estate_custom is the default App.chack it. 
<br>
NB:<br>
The first step of module creation is to create its directory. In the tutorials directory, add a new directory estate.

A module must contain at least 2 files: the __manifest__.py file and a __init__.py file. The __init__.py file can remain empty for now and we’ll come back to it in the next chapter. On the other hand, the __manifest__.py file must describe our module and cannot remain empty. Its only required field is the name, but it usually contains much more information.

Take a look at the CRM file as an example. In addition to providing the description of the module (name, category, summary, website…), it lists its dependencies (depends). A dependency means that the Odoo framework will ensure that these modules are installed before our module is installed. Moreover, if one of these dependencies is uninstalled, then our module and any other that depends on it will also be uninstalled. Think about your favorite Linux distribution package manager (apt, dnf, pacman…): Odoo works in the same way.


1.After install module Activate the developer mode (with assets) from Settings and Update Apps List from navbar.
<img src='https://www.odoo.com/documentation/17.0/_images/settings.png'><br>
2.Demo Manifest:<a href='https://www.odoo.com/documentation/17.0/developer/reference/backend/module.html#reference-module-manifest'> Read the article.</a>

Make sure you add 'depends': ['base'].<br>

3.Add custom model pwd in odoo.conf.
see <br>
<a href="../demo-odoo.conf">demo-odoo.conf</a>
<br>
Yes, now we can create our first model 🤗.