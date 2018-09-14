# Diário Oficial

**Diário Oficial** is the Brazilian government gazette, one of the best places to know the latest actions of the public administration, with distinct publications in the federal, state and municipal levels.

Even with recurrent efforts of enforcing the [Freedom of Information legislation](http://www.acessoainformacao.gov.br/assuntos/conheca-seu-direito/principais-aspectos/principais-aspectos) across the country, official communication remains - in most of the territories - in PDFs.

The goal of this same project is to upgrade **Diário Oficial** to the year when it gets published, making accessible information that is currently only available.


## Build and Run

If you want to understand how Diário Oficial works, you'll want to get the source, build it, and run it locally.

The only prerequisites are [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/overview/), which are the tools responsible for installing all the other dependencies.

After you cloned the repository, you may want to run the following from the source folder:

```console
$ make setup
$ docker-compose up
```

Once the download and building processes are finished, the processing tasks should start running in background, and the web server should be available at http://localhost:8080/.

### Upload files to Digital Ocean Spaces

The files are upload using `boto3` API for AWS S3, given that it is compatible with Digital Ocean Spaces.

In order to enable this functionality, you need to set the following environment variables

```sh
FILES_STORE=''
SPACES_NAME=your-spaces-name
SPACES_ACCESS_KEY_ID=your-key
SPACES_SECRET_ACCESS_KEY=your-key
```

 - `FILES_STORE`: if set to false or an empty string, Scrapy does not save the data locally.
 - `SPACES_ACCESS_KEY_ID`: an access key obtained in the `API` section your Digital Ocean Dashboard
 - `SPACES_SECRET_ACCESS_KEY`: an secret access key obtained in the `API` section your Digital Ocean Dashboard

 An example would be the following:

 ```sh
SPACES_NAME=test-scrapy
SPACES_ACCESS_KEY_ID=T3JRHS6M4CFIUH3EM62K
SPACES_SECRET_ACCESS_KEY=p4arD3AxCupbZxK4Iz/nlHAABaarIEoC4YQdD9G0Tl2
 ```

## Contributing

If you are interested in fixing issues and contributing directly to the code base, please see the document [CONTRIBUTING.md](CONTRIBUTING.md).
