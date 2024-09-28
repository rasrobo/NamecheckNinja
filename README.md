# NamecheckNinja

NamecheckNinja is a Python script that allows you to effortlessly manage your Namecheap domains by fetching domain information using the Namecheap API. It provides a sleek and intuitive way to view and analyze your domain portfolio, including domain expiration dates, auto-renewal status, WhoisGuard protection, and more.

## Features

- Stealthily fetches domain information from your Namecheap account using the API
- Displays a ninja-style table of all your domains with key details
- Sorts domains by expiration status (expired first) and expiration date
- Enumerates the list of domains for easy reference
- Provides a count of total active (non-expired) domains
- Supports verbose output for debugging and troubleshooting
- Easy to integrate with your existing Python projects

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/rasrobo/NamecheckNinja.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Update the script with your Namecheap API credentials:
   - Replace `api_username`, `api_key`, `username`, and `client_ip` with your actual values.

## Usage

Run the script with the following command:
```
python namecheckninja.py
```

To enable verbose output for debugging, use the `--verbose` flag:
```
python namecheckninja.py --verbose
```

## Example Output

```
+---------+-----------------------+------------+------------+-------------+------------+-------------+--------------+-------------+------------+
| Index   | Domain Name           | Created    | Expires    | IsExpired   | IsLocked   | AutoRenew   | WhoisGuard   | IsPremium   | IsOurDNS   |
+=========+=======================+============+============+=============+============+=============+==============+=============+============+
| 1       | example1.com          | 01/01/2022 | 01/01/2023 | true        | false      | false       | ENABLED      | false       | true       |
+---------+-----------------------+------------+------------+-------------+------------+-------------+--------------+-------------+------------+
| 2       | example2.net          | 02/15/2022 | 02/15/2024 | false       | false      | true        | ENABLED      | false       | true       |
+---------+-----------------------+------------+------------+-------------+------------+-------------+--------------+-------------+------------+
| 3       | example3.org          | 03/30/2022 | 03/30/2023 | false       | false      | true        | NOTPRESENT   | false       | true       |
+---------+-----------------------+------------+------------+-------------+------------+-------------+--------------+-------------+------------+
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Donations

If you find NamecheckNinja useful and would like to support its development, you can buy me a coffee! Your support is greatly appreciated.

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/default-orange.png)](https://buymeacoffee.com/robodigitalis)

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

NamecheckNinja is provided as-is and is not officially endorsed or supported by Namecheap. Use it at your own risk. Make sure to comply with Namecheap's API usage policies and terms of service.

## Keywords

namecheckninja, namecheap domain management, python namecheap script, namecheap api, domain expiration, auto-renewal, whoisguard, github namecheap script, namecheap domain portfolio
