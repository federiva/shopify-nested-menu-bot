# shopify-nested-menu-bot

This is a bot to create [nested menus](https://help.shopify.com/en/themes/development/building-nested-navigation) in the admin side of shopify stores. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* This bot has been built on Ubuntu 18.04 using Python 3.7.5 and it has not been tested on other OSS. 
* Dependencies used are listed in the requirements.txt file.  

#### Input Data and its relation to the data in the store

1. The data to be used needs to be in a dictionary format in which keys are First Level data and values the Second Level Data. For example: 

```
data_fruits = {'Banana': ['Ecuador', 'Colombia', 'Argentina', 'Brasil', 'Indonesia'],
               'Kiwi': ['New Zealand', 'Australia', 'New Guinea'],
               'Lemon': ['Argentina', 'USA', 'Paraguay', 'Ukraine']}
```
This means that Banana, Kiwi and Lemon are first level values while the values ['Ecuador', 'Colombia', ... ] are the second level values.

2. The data (First Level and second level) must be written exactly as the collection, tags, etc. names in the Shopify store. This means that if we are using the previous example data this means that in the case of collections, our Shopify store must have the following structure. 

Banana  
|------ Ecuador  
|------ Colombia  
|------ Argentina  
|------ Brasil  
|------ Indonesia  

And we must need to have the following collections already created in the store: 
* Banana
* Banana Ecuador (or for example Banana > Ecuador)
* Banana Colombia
* Banana Argentina
* Banana Brasil
* Banana Indonesia



### Installing

1. Recommended: Use a python IDE which uses an interactive console (Spyder, Pycharm, etc.)

2. Clone the repository
```
git clone https://github.com/federiva/shopify-nested-menu-bot
```
3. Recommended: Create a virtual [environment](https://docs.python.org/3/library/venv.html)

4. Install dependencies from requirements.txt to your virtual environment or directly into your global environment.
```
 pip install -r requirements.txt 
```
5. Install Mozilla's [geckodriver](https://github.com/mozilla/geckodriver/releases)

6. Add the geckodriver to your PATH

7. Using your IDE and open shopify_nested_menu_bot.py

* Set your credentials as global variables 
```
ADMIN_URL = 'https://your-store.myshopify.com/admin/'
RAP = 'your-user'
PAR = 'your-password'
```
* Optional: Set the path to a DB
## Examples

### Initializing the BOT
```
# Using the IDE or an Interactive Python Console, source the code
# Initializing
shopify_bot = bot_collections(admin_site=ADMIN_URL, RAP=RAP, PAR=PAR, PATH_LOCAL_DB=PATH_LOCAL_DB)
# Login using the credentials
shopify_bot.login()
# Go to the NEW Menu page
shopify_bot.go_to_menus()

```
### Creating First Level Menus 
1. Preparing data and inserting the menu name
```
# Using the fruits data
data_fruits = {'Banana': ['Ecuador', 'Colombia', 'Argentina', 'Brasil', 'Indonesia'],  
               'Kiwi': ['New Zealand', 'Australia', 'New Guinea'],  
               'Lemon': ['Argentina', 'USA', 'Paraguay', 'Ukraine']}  
# Creating a menu
shopify_bot.add_menu_name(menu_name='Fruits')
```
2.
  * Using default option and join_by arguments and without setting the _prepend or append_ arguments.
```
# Adding first level data
shopify_bot.add_data_first_level(data_in= data_fruits)
```
This must link the Banana, Kiwi and Lemon first level values to collections already created which match exactly the same names

  * Using the default on the option and join_by arguments but setting the _prepend argument: 
```
# Adding first level data
shopify_bot.add_data_first_level(data_in= data_fruits, _prepend='Foods')
```
This will create once again first level menus named Banana, Kiwi and Lemon. But now they will map to the 
Foods > Banana, Foods > Kiwi and Foods > Lemon collections previously created in the store.  
Note here that we can set up a custom join_by argument, for example instead mapping to Foods > Banana we can map to Foods | Banana if we set the join_by= ' | '
#### Note on the creation of first level data
* If you're only creating first level menus with this bot then you will note that you'll have some mock_menus created, you can delete them manually or running the following method
```
shopify_bot.remove_all_mock_menus(data_in= data_fruits)
```
* If you're going to create second level data afterwards then you'll need to manually reorder these <mock menus> as child of their respective parents (This is because we need the parent menus to be 'opened' with child menus in order to create child menus to the menus)

### Creating Second Level Menus
1. Using the data_fruits object and being consistent with the use of the _prepend and append_ arguments used at the first level
```
shopify_bot.add_data_second_level(data_in= data_fruits, _prepend='Foods')
```
2. Removing the mock menus created before
```
# Removing the mock menus
shopify_bot.remove_all_mock_menus(data_in= data_fruits)
```
3. Saving changes (this can be done manually too using the driver) 
```
# Saving the changes
shopify_bot.save_changes()
```
## Authors

* **Federico Rivadeneira** - *Initial work* - [federiva](https://github.com/federiva)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
