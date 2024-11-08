Title: Explorations with Pelican (part two)
Date: 2020-05-28 17:00
Category: tech
Tags: tech, python, docker, css
Slug: pelican_part_two
Authors: james
Summary: Working with Pelican plugins for dithering and live reload

In my [last post about Pelican](https://jameslmart.in/pelican) I mentioned my Docker setup and that I hadn't looked into live reloading. As it turns out, you only need one line to run the Pelican server with live reload. Previously I had this `make` command:
```
serve: ## Regen and serve blog, to be run in running Docker container
	pelican /home/app/source/content -o /home/app/public -s /home/app/pelicanconf.py
	pelican -l /home/app/source/content -o /home/app/public -s /home/app/pelicanconf.py -p 8000 -b 0.0.0.0
```

I was doing some digging into the `tasks.py` file that ships with Pelican and found there was a `livereload` task. I wasn't exactly sure how that specific task gets invoked, but after a few google searches I found that it's a recent feature merged in 2019. After another more thorough reading of `pelican --help`, I realized it's just a flag that you pass when starting the server.

Now I run:

```
serve: ## Serve blog with livereload, to be run in running Docker container
	pelican -lr /home/app/source/content -o /home/app/public -s /home/app/pelicanconf.py -p 8000 -b 0.0.0.0 &
```

When I'm in the running Docker container with my Python and Pelican environment to run the server with live reload. I bind the server to all the IP addresses on the local (virtual/Docker) machine and expose the port the Docker server runs on. I also background this process so I can continue to hack around the Docker container if need be.

### Plugins

I also spent some time working with Pelican plugins. [LOW&larr;TECH MAGAZINE](https://solar.lowtechmagazine.com/) has a great method of reducing page size through dithering of images, and wrote a [Pelican plugin](https://github.com/lowtechmag/solar-plugins/tree/master/dither) to run the duthering. Some images I want dithered, others I do not, but regardless I wanted to see what it takes to get plugins working.

The first step I took was to poke around the plugin code itself. Luckily, Low Tech included a README for their plugin and specified which Python packages the plugin relied on. Since I'm working with Docker, I added an additional RUN command to my Dockerfile to perform a second `pip install`. Hopefully this allows Docker to cache build steps and not have to reinstall the Pelican wheel every time a dependency of a plugin gets changed. With the revised Dockerfile, I rebuilt my Pelican environment.

The next step was to modify my make command to stand up said Pelican docker image to volume mount the directory containing the plugins. This process is exactly like the process I described to volume mount the themes directory. My Makefile simplifies these Docker commands, here's a snippet:

```
run-docker:
	@-docker rm -f $(DOCKER_CONTAINER_NAME)
	@docker run --rm \
		$(DOCKER_OPTS) \
		$(DOCKER_PORTS) \
 		--name=$(DOCKER_CONTAINER_NAME) \
		--workdir /home/app/ \
		$(DOCKER_IMAGE) $(DOCKER_CMD)

build-pelican: ## Build the latest Pelican image
	docker build -t pelican -f ./Dockerfile .

dev: DOCKER_CONTAINER_NAME=pelican
dev: DOCKER_OPTS=-it -v `pwd`:/home/app/ \
	-v `pwd`/../pelican-themes:/home/themes \
	-v `pwd`/../pelican-plugins:/home/plugins \
	--workdir /app/
dev: DOCKER_PORTS=-p $(APP_PORT):8000
dev: DOCKER_CMD=bash
dev: run-docker
dev: ## Run Docker image for Pelican to generate local content
```

A `make dev` will now stand up and start a bash shell in a Python environment with Pelican and any dependencies installed; themes and plugins will be mounted horizontally to the blog content. Next, I modified the Pelican config at `pelicanconf.py` to specify the paths of the plugins and enable the ones that are mounted. I needed to add these lines, as well as a few others specific to the dither plugin:

```
PLUGIN_PATHS = ['/home/plugins']
PLUGINS = ['dither','addressable_paragraphs']
```

After a little hacking on the dither plugin, I now can either choose which images to dither, as well. Transparent diagrams are ruined by dithering but the plugin is incredibly useful for minimizing the footprint of the web pages.

### TODO
My main next todo for improving the site is to fix the width of the "highlight" divs that Pelican generates for code blocks. They really ruin the responsiveness of the web pages where I put example code, like this one. Bear with me until I get it right.
