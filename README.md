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

### Upload files to Google Cloud Storage

If you don't want to save the pdfs locally, uploading them to a bucket in Google Cloud Storage can be done.

Scrapy does the uploading, you only need to set 3 environemnt variables, `FILES_STORE`, `GCS_PROJECT_ID` and `GOOGLE_APPLICATION_CREDENTIALS`.

 - `FILES_STORE`: the bucket name, e.g. `gs:/<BUCKET-NAME>/`
 - `GCS_PROJECT_ID`: the Google Cloud Storage project ID
 - `GOOGLE_APPLICATION_CREDENTIALS`: the Google application credentials json file. It needs to be at the same directory level as `diario-oficial-auth.json.sample`.

 An example would be the following:

 ```sh
GCS_PROJECT_ID=diario-oficial-2018
FILES_STORE=gs://test-diario-oficial/
GOOGLE_APPLICATION_CREDENTIALS=diario-oficial-auth.json
 ```

If no interest is present in this feature, simply leave these 3 variables values as `null`

## Contributing

If you are interested in fixing issues and contributing directly to the code base, please see the document [CONTRIBUTING.md](CONTRIBUTING.md).
