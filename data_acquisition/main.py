from functions import *
import json
from datetime import datetime

if __name__ == "__main__":
    start = datetime.now()

    # Specify the file path where you want to save the data
    file_path = "data.csv"

    years = [str(year) for year in range(1953, 2025)]
    for year in years:
        year_result = []

        html_text = get_blade_size_finder_response(year, '', '').text
        car_makers = extract_car_makers_from_html(html_text)
        for maker in car_makers:
            html_text = get_blade_size_finder_response(year, maker, '').text
            car_models = extract_models_from_html(html_text)
            for model in car_models:
                html_text = get_blade_size_finder_response(year, maker, model).text
                blade_sizes = extract_blade_sizes(html_text)
                year_result.append({'year': year, 'make': maker, 'model': model, 'blade_sizes': blade_sizes})

        for res in year_result:
            # Creat line to append to the csv file
            line = "{},{},{},{},{},{}\n".format(
                res['year'], res['make'], res['model'],
                res['blade_sizes']['driver'],
                res['blade_sizes']['passenger'],
                res['blade_sizes']['rear'])

            # Append line to the file
            with open(file_path, "a") as file:
                file.write(line)

        # Save time until this year in minutes
        current_time = (datetime.now() - start).seconds
        print(f"Finished year {year} in\t{current_time//60} minutes and {current_time%60} seconds")



    # # Save the list of dictionaries to the file
    # with open(file_path, "w") as file:
    #     json.dump(result, file)
    #
    # print(f"Data saved to {file_path}")
    # print(f"Time taken: {datetime.now() - start}")
