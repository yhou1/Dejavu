#!/bin/sh

# surfaces.sh
#
# Output road-surface data from Open Street Map (OSM).
#
# Set some default variables:

temp_dir="/tmp"
output_dir="."
verbose=""
usage="$0 [-h] [-v] [-t temp/dir] [-o output/dir] <input-file.osm.pbf>

  -h      Show this help.
  -v      Verbose mode, print details about progress.
  -t      Use another directory for temporary files. Default: /tmp/
  -o      Use anotehr directory for output files. Default: ./
"
# Store our the program path.
pushd `dirname $0` > /dev/null
my_path=`pwd -P`
popd > /dev/null
script_path=`dirname $my_path`
script_path="${script_path}/bin"

##
# Allow the user to configure our variables via command-line options.
##
OPTIND=1         # Reset in case getopts has been used previously in the shell.
while getopts "h?vt:o:" opt; do
  case "$opt" in
  h|\?)
    echo usage >&2
    exit 1
    ;;
  v)  verbose="-v"
    ;;
  o)  output_dir=$OPTARG
    ;;
  t)  temp_dir=$OPTARG
    ;;
  esac
done
shift $((OPTIND-1))
[ "$1" = "--" ] && shift
# End configuration

##
# Process each file in the input list
##
for input_file in "$@"
do
  # Strip off the file extensions.
  filename=`basename -s .pbf $input_file`
  filename=`basename -s .osm $filename`

  # Make a temporary directory.
  mkdir $temp_dir/$filename

  # Take the following processing steps first:
  # 1. Calculate the curvature
  # 2. Add 'length' fields to the data.
  # 3. Sort the items by their curvature value.
  # 3. Output a KML file showing the surfaces for all roads.
  $script_path/curvature-collect --highway_types 'motorway,trunk,primary,secondary,tertiary,unclassified,residential,service,motorway_link,trunk_link,primary_link,secondary_link,service' $verbose $input_file \
    | $script_path/curvature-pp add_segments \
    | $script_path/curvature-pp add_segment_length_and_radius \
    | $script_path/curvature-output-kml-surfaces \
    > $temp_dir/$filename/doc.kml
  # Zip the KML into a KMZ
  zip -q $output_dir/$filename.surfaces.kmz $temp_dir/$filename/doc.kml
  # Delete our temporary file.
  rm $temp_dir/$filename/doc.kml
  rmdir $temp_dir/$filename

done