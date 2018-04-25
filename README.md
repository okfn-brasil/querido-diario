# Diário Oficial

**Diário Oficial** is the Brazilian government gazette, one of the best places to know the latest actions of the public administration, with distinct publications in the federal, state and municipal levels.

Even with recurrent efforts of enforcing the [Freedom of Information legislation](http://www.acessoainformacao.gov.br/assuntos/conheca-seu-direito/principais-aspectos/principais-aspectos) across the country, official communication remains - in most of the municipalities - in PDFs.

The goal of this same project is to upgrade **Diário Oficial** to the year when it gets published, making accessible information that is currently only available.

## Build and Run

If you want to understand how Diário Oficial works, you'll want to get the source, build it, and run it locally.

The only prerequisites are [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/overview/), which are the tools responsible for installing all the other dependencies.

After you cloned the repository, you may want to run the following from the source folder:

```console
$ make setup
$ docker-compose up
```

Once the download and building processes are finished, the processing tasks should start running in background and the webserver should be available at http://localhost:8080/.


## Contributing

If you are interested in fixing issues and contributing directly to the code base, please see the document [CONTRIBUTING.md](CONTRIBUTING.md).

## Running the Project Without Docker

Even if your environment is working with the setup described above - and it should be, because you'll probably want to test your work inside docker before sending PR's - sometimes you'd like to run the project without docker for some reason, for example to have an easier time debugging python code. In this section we will explain one way to do this. Note that you'll need the database container for this to work, i.e. be sure to follow through the normal docker setup before following the steps below.

In the project directory, run:

```console
$ python -m venv venv
```

This command creates a virtual environment for the project. To activate it, do this:

```console
$ source venv/bin/activate
```

Now that your virtual environment is active you need to install the `data_collection` dependencies:

```console
$ pip install -r processing/requirements.txt
```

Then update Scrapy's settings (found in the `processing/data_collection/gazette/` directory). You need to set `FILES_STORE` to a valid directory in your computer.

You'll also need to know the database container's (postgres) IP:

```console
$ docker ps -a # to help you find the diariooficial_postgres_????
$ docker inspect <container_name> | grep '"IPAddress"'
```

Finally, you can run the scrapper for Porto Alegre using this command:

```
$ cd processing/data_collection
$ DATABASE_URL=<DATABASE_URL> PYTHON_PATH="$PYTHONPATH:../" python -m scrapy crawl rs_porto_alegre
```

Where `<DATABASE_URL>` is equal to the value present in your `.env` file, replacing the host (currently `postgres`) with the IP you've found above.

The `PYTHON_PATH` override is necessary to correctly expose the database module.

Happy debugging!
