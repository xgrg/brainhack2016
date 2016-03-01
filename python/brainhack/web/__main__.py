
import sys
import argparse
import brainhack.web
parser = argparse.ArgumentParser(description='Runs the web server')
parser.add_argument("--port", help="Port", default=8888, required=False)
parser.add_argument("--max-preview", dest='maxitems', default=500, type=int, help="How many files to preview", required=False)
parser.add_argument("--repository", dest='repository', type=str, help="Repository folder", required=True)
parser.add_argument("--hierarchy", dest='hierarchy', type=str, help="Output hierarchy json", required=True)

args = parser.parse_args()
brainhack.web.main(args)
