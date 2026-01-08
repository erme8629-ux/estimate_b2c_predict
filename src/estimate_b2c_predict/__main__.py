import argparse, textwrap
import sys

argparser = argparse.ArgumentParser(description='estimate_b2c_predict', epilog=textwrap.dedent('''
Example:

'''),formatter_class=argparse.RawTextHelpFormatter)
subparsers = argparser.add_subparsers(dest='mode')

formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=100)

arg_get_b2c = subparsers.add_parser('estimate_b2c', help='estimate_b2c', formatter_class=formatter)
arg_get_b2c._action_groups.pop()
required = arg_get_b2c.add_argument_group('required arguments')
optional = arg_get_b2c.add_argument_group('optional arguments')
required.add_argument('--country', metavar='', type=str, help='country', required=True)
required.add_argument('--date', metavar='', type=str, help='date', required=True)
required.add_argument('--ID', metavar='', type=str, help='ID', required=True)
required.add_argument('--age', metavar='', type=int, help='age', required=True)
required.add_argument('--km', metavar='', type=int, help='km', required=True)
optional.add_argument('--output_path', metavar='', type=str, help='output_path', required=False)


args = argparser.parse_args() 
mode=args.mode

if mode == 'estimate_b2c':
    from estimate_b2c_predict.estimate_b2c import call_estimate_b2c

    input_dict = {
        "country": args.country,
        "date": args.date,
        "ID": args.ID,
        "age": args.age,
        "km": args.km
    }

  
    call_estimate_b2c(input_data=[input_dict])

"""
if mode=='estimate_b2c':
	from estimate_b2c_predict.estimate_b2c import estimate_b2c
	country = args.country
	date = args.date
	ID = args.ID
	age = args.age
	km = args.km
	output_path = args.output_path
	


	
	estimate_b2c(country, date, ID, age, km)
"""	
	


