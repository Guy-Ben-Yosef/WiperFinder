from bs4 import BeautifulSoup
import requests


def get_blade_size_finder_response(year, make, model):
    """
    Perform a POST request to retrieve blade size finder response from a specified URL.

    :param year:  The year of the car.
    :param make:  The make of the car.
    :param model: The model of the car.
    :return: requests.Response: The response object containing the server's response.

    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.findmywipers.com/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.findmywipers.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    data = {
        'search_url': 'https://www.findmywipers.com/',
        'action': 'submit',
        'bf-year': year,
        'bf-make': make,
        'bf-model': model,
    }
    response = requests.post('https://www.findmywipers.com/blade-size-finder/', headers=headers, data=data)
    return response


def extract_car_makers_from_html(html_content):
    """
    Extract carmakers from HTML Content

    This function takes an HTML content string as input, parses it, and extracts a list of carmakers
    found within a specific <div> element with class "bf_makeOptonsHtml" in the HTML content.

    :param  html_content: A string containing the HTML content to be parsed and searched.
    :return list:         A list of carmakers extracted from the HTML content.
    """
    car_makers = []

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the <div> with class "bf_makeOptonsHtml"
        make_options_div = soup.find('div', class_='bf_makeOptonsHtml')

        if make_options_div:
            # Find all <option> elements within the <div>
            option_elements = make_options_div.find_all('option')

            # Loop through the <option> elements and extract carmakers
            for option in option_elements:
                value = option.get('value')
                if value and value != "Make":
                    car_makers.append(value.strip())

    except Exception as e:
        print(f"An error occurred: {e}")

    return car_makers


def extract_models_from_html(html_content):
    """
    Extract Model Options from HTML Content

    This function takes an HTML content string as input, parses it, and extracts a list of model options
    found within a specific <div> element with class "bf_modelOptonsHtml" in the HTML content.

    :param   html_content: A string containing the HTML content to be parsed and searched.
    :return: list:         A list of model options extracted from the HTML content.
    """
    model_options = []

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the <div> with class "bf_modelOptonsHtml"
        model_options_div = soup.find('div', class_='bf_modelOptonsHtml')

        if model_options_div:
            # Find all <option> elements within the <div>
            option_elements = model_options_div.find_all('option')

            # Loop through the <option> elements and extract model options
            for option in option_elements:
                value = option.get('value')
                if value and value != "Model":
                    model_options.append(value.strip())

    except Exception as e:
        print(f"An error occurred: {e}")

    return model_options


def extract_blade_sizes(html_content):
    """
    Extract blade sizes from HTML content.

    :param html_content: A string containing the HTML content to be parsed and searched.
    :return dict: A dictionary containing the blade sizes for driver, passenger, and rear wipers.
    """
    blade_sizes = {}

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the <header> element with class "search_header"
        header_element = soup.find('header', class_='search_header')

        if header_element:
            # Find all <div> elements with class "blade_size"
            blade_size_elements = header_element.find_all('div', class_='blade_size')

            # Loop through the <div> elements and extract blade sizes
            for blade_size_element in blade_size_elements:
                blade_type = blade_size_element.get_text().split()[0].strip()
                blade_size = blade_size_element.find('strong').get_text().strip()
                blade_sizes[blade_type.lower()] = blade_size

            # If any of the blade sizes are missing, add an empty string to the dictionary
            for possible_key in ['driver', 'passenger', 'rear']:
                if possible_key not in blade_sizes:
                    blade_sizes[possible_key] = ''

    except Exception as e:
        print(f"An error occurred: {e}")

    return blade_sizes
