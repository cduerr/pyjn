## pyjn

pyjn is a command line tool that allows to manipulate json data using python.

### Examples

```
cat estimate.json | pyjn.py "sum([i['price'] for i in data['items']])"
cat inventory.json | pyjn.py "{k:v for k,v in data.get('widgets').items() if v != 'blah'}"
```

```
./pyjn.py "list(zip(*data[::-1]))" -i "[[1,2,3],[4,5,6],[7,8,9]]"
./pyjn.py "list(zip(*data[::-1]))" -i ./matrix.json
```

```
./pyjn.py -i ./matrix.json -e  # invoke editor to edit python code
```

```
cat ./results.json | ./pyjn.py "jmespath.search('matrix', data)"
```

### Installation

```
# change to the folder where you want to install pyjn
git clone git@github.com:cduerr/pyjn.git 
cd pyjn
pipenv install
```
