# Hero_Name_Recognition

## Env 
```
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
pip install -r requirements
```

## Crawl data
When need download data about hero
```
python crawl_hero_avatar.py
```

## Run predict 
```
python test.py 
```

## Run eval from predict 
```
python eval.py 
```