#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:59:42 2019

@author: trona
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 17:47:53 2019

@author: federiva at github.com
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3

ADMIN_URL = 'https://your-store.myshopify.com/admin/'
RAP = 'your-user'
PAR = 'your-password'
PATH_LOCAL_DB = None

class bot_collections:
    
    
    def __init__(self, admin_site, RAP, PAR, open_driver=True, PATH_LOCAL_DB='None'):
        
        self.PATH_LOCAL_DB = PATH_LOCAL_DB
        if open_driver:
            self.driver = webdriver.Firefox()
            self.wait = WebDriverWait(self.driver, 10)
            self.driver.get(admin_site)
            self.RAP = RAP
            self.PAR = PAR
            self.home_url = admin_site
        else:
            pass



    def login(self):
        '''
        Login into the admin side of the shopify store using the RAP and PAR 
        attributes

        Returns
        -------
        None.

        '''
        rap = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#account_email')))
        rap.send_keys(shopify_bot.RAP)
        
        next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH,'.//button[contains(text(), "Next")]')))
        next_button.click()
    
        par = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#account_password')))
        par.send_keys(shopify_bot.PAR)    
        
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH,'.//button[contains(text(), "Log in")]')))
        login_button.click()
        
        return

    def go_to_menus(self):
        '''
        Go to the URL for adding a new menu

        Returns
        -------
        None.

        '''
        self.driver.get('{}{}'.format(self.home_url, 'menus/new'))

    def connect_to_db(self, cursor=False):
        '''
        Connects to the database giving trough the path_local_db creating
        the connection and cursor attributes (this last one is optional)

        Parameters
        ----------
        cursor : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        '''
        self.connection = sqlite3.connect(self.path_local_db)
        if cursor:
            self.cursor = self.connection.cursor()
            return
        return
    
    def disconnect_from_db(self):
        '''
        Disconnects the cursor and the connection to the database

        Returns
        -------
        None.

        '''
        try:
            self.cursor.close()
        except:
            pass
        try:
            self.connection.close()
        except:
            pass
        return
    
    def add_menu_name(self, menu_name):
        '''
        Add the menu name

        Parameters
        ----------
        menu_name : string
            Name of the Menu

        Returns
        -------
        None.

        '''
        name_input = self.driver.find_element_by_id('menu-item-name')
        name_input.send_keys(menu_name)
        return
    
    def add_element_first_level(self, name_in, option='colecciones',_prepend=None, append_=None, join_by= ' > ', is_mock=False):
        '''
        Add an element to the created menu at the first level
        
        Parameters
        ----------
        name_in : string
            The name of the first level menu
        
        option : string (Default for spanish: colecciones) case-insensitive
            This option is the name of the option choosed to filter the links
        
        _prepend : string (Default: None) Cannot be used along with append_
            This is a string to prepend to the name_in value, for example: 
                if name_in is Bananas then _prepend = Fruits
            This entire name plus the join_by argument will match the name that
            the previously created collection has. In this case, for example if 
            we set the following parameters: 
                name_in='Bananas', _prepend='Fruits', join_by=' > '
            Then the collection name in the shopify store will match exactly to:
                Fruits > Bananas
                
        append_ : string (Default: None) Cannot be used along with _prepend
            This is a string to append to the name_in value. The use case is 
            the same but opposite to the use in _prepend: Example
            name_in='Bananas', append_='Ecuador', join_by=' > ' will result in 
                Bananas > Ecuador
            And this will match exactly the collection name in the store
        
        join_by : string (Default: ' > ')
            This string is used to join the name_in + append_ or _prepend values
            in order to build the collection names.
            
        is_mock : bool (Default: False)
            If set to true then creates a menu with the _mock string appended
            to it. This is used just for creating second level menus and it is
            not handled by the user.
        '''
        
        # We can only set one condition
        assert(not _prepend or not append_)
        try:
            button_add_menu_element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ui-button--full-width')))
        except:
            try:
                button_add_menu_element = shopify_bot.driver.find_elements_by_xpath('.//li[@class="menu__list-item-add"]//button[contains(@class,add-button)]')
                button_add_menu_element = [x for x in button_add_menu_element if 'Agregar' in x.text or 'Add' in x.text]
                if len(button_add_menu_element) == 1: 
                    button_add_menu_element = button_add_menu_element[0]
                else:
                    raise Exception('Can\'t find the button to add a new element')
            except:
                raise Exception('Can\'t find the button to add a new element')
        button_add_menu_element.click()
        
        input_name = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#addMenuItemName'))) 
        if is_mock:
            input_name.send_keys(name_in + '_mock')
        else:
            input_name.send_keys(name_in)
        
        if _prepend: 
            name_in = join_by.join([_prepend.strip(),name_in.strip()])
        elif append_:
            name_in = join_by.join([name_in.strip(), append_.strip()])
            
        link_menu = self.driver.find_element_by_id('addMenuItemLink')
        link_menu.send_keys(name_in)
        
        # Get options
        sleep(5)
        options = self.driver.find_elements_by_xpath('.//li[@role="option"]/a')
        choosed_option = [x for x in options if option.strip().lower() in x.text.strip().lower()]
        assert(len(choosed_option) == 1)
        choosed_option[0].click()
        sleep(5)
        # choose 
        popup_options = self.driver.find_elements_by_xpath('.//ul[contains(@id,popover-dropwdown)]//li')
        choosed_option = [x for x in popup_options if x.text == name_in]
        if len(choosed_option) == 1: 
            choosed_option[0].click()
            try:
                add_button = self.driver.find_element_by_xpath('.//div[@class="ui-modal__footer"]//button[@name="commit"]')
                add_button.click()
                return
            except:
                pass
            return
        else:
            raise Exception('The option {} has not been found among the listed links'.format(name_in))
        return
    
        
    def add_element_second_level(self, name_in, parent_name, option='colecciones', _prepend=None, append_=None, join_by= ' > '):
        '''
        Add an element to the created menu at the second level
        
        Parameters
        ----------
        name_in : string
            The name of the first level menu
        
        parent_name : string
            The name of the parent menu on which the second level data will be 
            appended
            
        option : string (Default for spanish: colecciones) case-insensitive
            This option is the name of the option choosed to filter the links
        
        _prepend : string (Default: None) Cannot be used along with append_
            This is a string to prepend to the name_in value, for example: 
                if name_in is Bananas then _prepend = Fruits
            This entire name plus the join_by argument will match the name that
            the previously created collection has. In this case, for example if 
            we set the following parameters: 
                name_in='Bananas', _prepend='Fruits', join_by=' > '
            Then the collection name in the shopify store will match exactly to:
                Fruits > Bananas
                
        append_ : string (Default: None) Cannot be used along with _prepend
            This is a string to append to the name_in value. The use case is 
            the same but opposite to the use in _prepend: Example
            name_in='Bananas', append_='Ecuador', join_by=' > ' will result in 
                Bananas > Ecuador
            And this will match exactly the collection name in the store
        
        join_by : string (Default: ' > ')
            This string is used to join the name_in + append_ or _prepend values
            in order to build the collection names.

        '''
        assert(not _prepend or not append_)
        assert(isinstance(name_in, str) and isinstance(parent_name, str))
        # Build the name to search the collection
        name_collection = []
        if _prepend: 
            name_collection = [_prepend.strip()]
        name_collection.append(parent_name.strip())
        name_collection.append(name_in.strip())
        if append_:
            name_collection.append(append_.strip())
        name_collection = join_by.join(name_collection)
        # Add input name
        input_name = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#addMenuItemName'))) 
        input_name.send_keys(name_in)
        # Add link
        link_menu = self.driver.find_element_by_id('addMenuItemLink')
        link_menu.send_keys(name_collection)
        # Get options
        sleep(5)
        options = self.driver.find_elements_by_xpath('.//li[@role="option"]/a')
        choosed_option = [x for x in options if option.strip().lower() in x.text.strip().lower()]
        assert(len(choosed_option) == 1)
        choosed_option[0].click()
        sleep(5)
        # Choose 
        popup_options = self.driver.find_elements_by_xpath('.//ul[contains(@id,popover-dropwdown)]//li')
        choosed_option = [x for x in popup_options if x.text == name_collection]
        if len(choosed_option) == 1: 
            choosed_option[0].click()
            try:
                add_button = self.driver.find_element_by_xpath('.//div[@class="ui-modal__footer"]//button[@name="commit"]')
                add_button.click()
                # return
            except:
                pass
            # return
        else:
            raise Exception('The option {} has not been found among the listed links'.format(name_collection))
 
    def remove_mock_menu(self, prefix_):
        '''
        Remove a mock menu

        Parameters
        ----------
        prefix_ : string
            The prefix that the previously created mock collection has, for example
            If we created the cats menu then the cats mock menu surely was:
                cats_mock
            So in order to remove it prefix_= 'cats'

        Returns
        -------
        None.

        '''
        menu_name = '{}_mock'.format(prefix_)
        # Look for the collection name
        mock_element = self.driver.find_elements_by_xpath('.//li[contains(@data-menu-item, "{}")]'.format(menu_name))
        if len(mock_element) == 1: 
            remove_button = mock_element[0].find_element_by_xpath('.//button[contains(@class, "remove")]')
            if remove_button:
                remove_button.click()
                accept_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, './/div[@class="buttons"]/a[contains(@class, "accept-modal")]')))
                if accept_button:
                    accept_button.click()
                else:
                    raise Exception('The accept button has not been found')
            else:
                raise Exception('The remove button has not been found')
            mock_element[0].click()
        else:
            raise Exception('Error: The element {} has not been found or more than one has been found with the same name'.format(menu_name))
        return
    
    def add_data_first_level(self, data_in, option='colecciones',_prepend=None, append_=None, join_by= ' > '):
        '''
        This is a wrapper method to add_element_first_level. It adds multiple
        first level menus.

        Parameters
        ----------
        data_in : Dictionary (k:string, v:list of strings)
            A dictionary with the data to add. The format is the following one:
                Key= First level name
                Values= Second level names (list)
        
        option : string (Default for spanish: colecciones) case-insensitive
            This option is the name of the option choosed to filter the links
        
        _prepend : string (Default: None) Cannot be used along with append_
            This is a string to prepend to the name_in value, for example: 
                if name_in is Bananas then _prepend = Fruits
            This entire name plus the join_by argument will match the name that
            the previously created collection has. In this case, for example if 
            we set the following parameters: 
                name_in='Bananas', _prepend='Fruits', join_by=' > '
            Then the collection name in the shopify store will match exactly to:
                Fruits > Bananas
                
        append_ : string (Default: None) Cannot be used along with _prepend
            This is a string to append to the name_in value. The use case is 
            the same but opposite to the use in _prepend: Example
            name_in='Bananas', append_='Ecuador', join_by=' > ' will result in 
                Bananas > Ecuador
            And this will match exactly the collection name in the store
        
        join_by : string (Default: ' > ')
            This string is used to join the name_in + append_ or _prepend values
            in order to build the collection names.

        Returns
        -------
        None.

        '''
        # Adding first level
        for i, kv in enumerate(data_in.items()):
            try:
                sleep(3)
                self.add_element_first_level(name_in=kv[0], _prepend= _prepend, append_= append_, join_by= join_by)
                sleep(3)
                self.add_element_first_level(name_in=kv[0], _prepend= _prepend, append_= append_, join_by= join_by, is_mock=True)
            except Exception as e:
                print(e)
                return
        return
        # Manually reorder items to create child elements of the desired ones. Also, 
        # manually delete those "mock" elements which don't really have a parent one

    
    def add_data_second_level(self, data_in, option='colecciones', _prepend=None, append_=None, join_by= ' > '):
        '''
        This is a wrapper method to add_element_second_level(). It adds multiple
        second level menus.

        Parameters
        ----------
        data_in : Dictionary (k:string, v:list of strings)
            A dictionary with the data to add. The format is the following one:
                Key= First level name
                Values= Second level names (list)
        
        option : string (Default for spanish: colecciones) case-insensitive
            This option is the name of the option choosed to filter the links
        
        _prepend : string (Default: None) Cannot be used along with append_
            This is a string to prepend to the name_in value, for example: 
                if name_in is Bananas then _prepend = Fruits
            This entire name plus the join_by argument will match the name that
            the previously created collection has. In this case, for example if 
            we set the following parameters: 
                name_in='Bananas', _prepend='Fruits', join_by=' > '
            Then the collection name in the shopify store will match exactly to:
                Fruits > Bananas
                
        append_ : string (Default: None) Cannot be used along with _prepend
            This is a string to append to the name_in value. The use case is 
            the same but opposite to the use in _prepend: Example
            name_in='Bananas', append_='Ecuador', join_by=' > ' will result in 
                Bananas > Ecuador
            And this will match exactly the collection name in the store
        
        join_by : string (Default: ' > ')
            This string is used to join the name_in + append_ or _prepend values
            in order to build the collection names.

        Returns
        -------
        None.

        '''
        # After reordering
        # Adding second level
        for i, kv in enumerate(data_in.items()):
            # Iterate over values
            for second_level_name in kv[1]: 
                sleep(5)
                add_buttons = self.driver.find_elements_by_class_name('menu__list-item-add')
                # Now the buttons must have the same name as the keys in our data dictionary
                # Extract the text from each button
                buttons_text = []
                for button in add_buttons:
                    try:
                        text = button.find_element_by_xpath('.//strong').text
                        buttons_text.append(text)
                    except:
                        buttons_text.append('')
                # Testing for the value that has exactly the same text inside
                test = [True if kv[0] == x else False for x in buttons_text]
                if any(test):
                    index = [i for i, x in enumerate(test) if x is True]
                    if len(index) == 1: 
                        button_to_click = add_buttons[index[0]]
                        button_to_click.click()
                    else:
                        raise Exception('Error, we found more than one button with the text: {} in it'.format(kv[0]))
                else:
                    raise Exception('Error, we didn\'t found a button with the text: {} in it'.format(kv[0]))
                sleep(5)
                self.add_element_second_level(name_in=second_level_name,parent_name=kv[0], _prepend= _prepend, append_= append_, join_by= join_by)
        
    def remove_all_mock_menus(self, data_in):
        '''
        This is a wrapper to remove_mock_menu. It removes multiple mock menus
        
        '''
        
        # Removing mock classes
        for i, kv in enumerate(data_in.items()):
            sleep(4)
            try:
                self.remove_mock_menu(prefix_=kv[0])
            except Exception as  e:
                print(e)
                pass
        return
    
    def save_changes(self):
        '''
        Save the changes on the menu being edited

        Returns
        -------
        None.

        '''
        save_changes = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._1eCDN > span:nth-child(1) > span:nth-child(1)')))
        save_changes.click()
        return
    
    def quit_bot(self):
        '''
        Close the selenium driver and also the database connection

        Returns
        -------
        None.

        '''
        self.driver.close()
        self.disconnect_from_db()    
        return
    
# Source the previous code and check for the examples at:
# https://github.com/federiva/shopify-nested-menu-bot/blob/master/README.md
        
    