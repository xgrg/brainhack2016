DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR="$(dirname "$DIR")"
python $DIR/python/kandu/web/__init__.py $@
