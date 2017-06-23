#!/usr/bin/python3
import argparse
import csv
from os import listdir
from os.path import isfile, join, basename
from subprocess import call
from multiprocessing import Pool
from functools import partial

import airspeed

def main():
	parser = argparse.ArgumentParser(description='Renders HTML templates to PNG with data from CSV.')
	parser.add_argument('-c', metavar='csv_path', type=str, default='data.csv', help='Path to CSV file from which to load data')
	parser.add_argument('-t', metavar='template_path', type=str, default='template.html', help='HTML template')
	parser.add_argument('-o', metavar='output_path', type=str, default='out', help='Output directory for PNGs')
	parser.add_argument('-x', metavar='width', type=int, default=1024, help='Width of output PNG')
	parser.add_argument('-y', metavar='height', type=int, default=768, help='Height of output PNG')

	args = parser.parse_args()

	html_template = load_template(args.t)
	csv_dict = load_csv_dict(args.c)

	generate_images(html_template, csv_dict, args.o, args.x, args.y)

def load_template(template_path):
	"""
	Loads a template from the template path.

	:param template_dir: The path to the HTML template to load
	:returns: An Airspeed template
	"""
	with open(template_path, 'r') as html_file:
		template = html_file.read() 

	return airspeed.Template(template)

def load_csv_dict(csv_file):
	"""
	Loads a CSV file as a list of dicts

	:param csv_file: Path to csv file
	:returns: list of dicts for the CSV
	"""
	with open(csv_file, 'r') as csvfile:
		csv_data = list(csv.DictReader(csvfile))
	return csv_data

def generate_images(template, csv_dict, output_dir, width, height):
	"""
	Generates images from a template, a dict of CSV rows, and
	outputs them to the given directory.

	:param template: Airspeed template to render.
	:param csv_dict: List of CSV rows to render.
	:param output_dir: Directory to output images to.
	"""

	generate_image_partial = partial(
		generate_image,
		template,
		output_dir,
		width,
		height,
	)

	with Pool() as pool:
		pool.map(generate_image_partial, csv_dict)

def generate_image(template, output_dir, width, height, row):
	rendered_html = template.merge(row)
	path = join(output_dir, '{}.png'.format(row['id']))
	args = (
		'google-chrome',
		'--headless',
		'--disable-gpu',
		f'--screenshot={path}',
		f'--window-size={width},{height}',
		'data:text/html,' + rendered_html,
	)
	call(args)


if __name__ == '__main__':
	main()