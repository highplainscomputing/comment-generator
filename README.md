# ML based Comment Generation
Machine learning pipeline for end-to-end Text Classification, Named-Entity Recognition and Comments Generation.

____
### Installation
**Required python version: 3.7 or higher and MongoDB**

```bash
git clone https://github.com/highplainscomputing/comment-generator.git
cd comment-generator
pip install -r requirements.txt
```

### Docker setup
**1. Clone repository**:
```bash
git clone https://github.com/highplainscomputing/comment-generator.git
```

**2. Build docker**:
```bash
cd comment-generator
docker build --tag comment-generator:latest .
```

**3. Run docker server**:
```bash
docker run -d -p 8080:8080 comment-generator:latest
```

**4. Use Docker Compose**:
It will create both the images (mongoDB and fastAPI) and start the containers.
```bash
docker-compose up -d
```

### Server API usage
#### Start server
```bash
uvicorn run_server:app --host "0.0.0.0" --port 8000
```
For Visualizing application Visit:
http://localhost:8000/docs

#### Endpoints
  - `/health` endpoint for checking server availability.
  
  - `/generate` endpoint for running complete pipeline and saving the result as json in MongoDB.
    Example input text:
    ```
    A Christmas tree that can receive text messages has been unveiled at London's Tate Britain art gallery.
    The spruce has an antenna which can receive Bluetooth texts sent by visitors to the Tate. The messages 
    will be "unwrapped" by sculptor Richard Wentworth, who is responsible for decorating the tree with broken 
    plates and light bulbs. It is the 17th year that the gallery has invited an artist to dress their Christmas
    tree. Artists who have decorated the Tate tree in previous years include Tracey Emin in 2002.
    ```
    Example Output
  - ```json
    {
    "entities":['NAME':'SIBTAIN RAZA'],
    "category": "politics"
    }
    
    ```
        
  - `/view` endpoint for Viewing list of stored results which include text category, ner and generated comment.
  - 
    Example outputs:
    ```json
    [{
    "id": "614a7804be790f5ae9de0e8b",
    "category": "politics",
    "entities": {
      "ORG": [
        "Sibtain Raza",
        "taliban"
      ]
    },
    "comment": "Sibtain Raza is a ML Engineer."}]
    
    ```
  
### Local usage (for debugging purposes)
Example of Running Pipeline on input text:
```bash
python main.py --input_text 'put your text here' --config config.yaml
```

### Run tests
```bash
cd comment-generator
pytest .
```

## Configuration and file structure
Project file structure is:
```
.
├── comment_generator
│    ├── __init__.py
│    ├── pipeline.py
│    ├── models
│    │    ├── __init__.py
│    │    ├── base.py
│    │    ├── classifier.py
│    │    └── generator.py
│    │    ├── ner.py
│    ├── utils
│    │    ├── __init__.py
│    │    ├── db_utils.py
│    │    ├── fastapi_models.py
│    │    └── parse_config.py
├── test
│   ├──__init__.py
│   ├──test_parse_config.py
│
└── docker-compose.yml
└── Dockerfile
└── config.yaml
└── README.md
└── main.py
└── run_server.py
└── requirements.txt

```

### Contributer
Sibtain Raza


