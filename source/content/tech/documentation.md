Title: Dear Lord, take minutes
Date: 2020-11-16 19:30
Category: tech
Tags: tech, writing, remote, skills
Slug: documentation
Authors: james
Summary: Documentation is more than READMEs

I've been reconnecting with some of my former co-workers and I've noticed an interesting thread across from these conversations. One person I've reconnected with was a former manager of mine who on my first day, tangentially related, sent me this short article on how [dev ops is everyone's job](https://opensource.com/article/17/7/state-systems-administration?imm_mid=0f591b&cmp=em-webops-na-na-newsltr_20170818). Little did she know how impressionable this would be. She also was the inspiration behind my first blog post on this site about not being blocked. I've taken to heart how backend engineers must be responsible for, or at least be knowledgable of, everything from the OS and runtime to the app code to monitoring and operating the code across deployment environments. While I could dedicate a separate blog post to this philosophy around operations, I want to focus on a similar trend I see emerging.

**In 2020 _documentation_ is everyone's job.** COVID has forced all engineering organizations to be remote. The software industry may be well equipped to be remote with respect to tools - we already have competency using version control, tracking work with JIRA, and using Slack to meet virtually but the hard part of building software is rarely actually building the software. The hardest parts of building software are resource and coordination problems, especially keeping all involved parties up to date with the latest information. And these issues are exasperated when remote.

While companies like GitLab have solid remote engineering practices and socialize them extensively, their model is not easily replicated across the industry. Building good remote culture takes additional process and a healthy amount of patience. As a tech lead on a small team, I've had to invest more heavily in project management and the tasks usually tackled by an engineering manager to fill communication gaps. My time is spent between clarifying the business impact of our work and balancing feature work with operational burden. Both tasks of tracking impact and making decisions are communication-heavy.

Communicating decisions verbally is ineffective - the "why" behind decisions being made is easily lost. Slack isn't much better, and "although digital media appears to sustain memory, it is more like oral communication in its evanescence" ([Sacasas](https://www.thenewatlantis.com/publications/the-analog-city-and-the-digital-city)). Where in an office we may have sat around our desks and debated development philosophy or drawn architecture diagrams on whiteboards to explain mental models, we lose the ad-hoc time when these concepts are communicated.

### Start somewhere

When was the last time you were in a meeting where someone took minutes? The act of opening a Google Doc, writing down the date and time of the meeting, the attendees, and at least a brief summary of what will be discussed will anchor a meeting to stay on task. If you take that first step, you will probably continue to write down other useful information. If the person who is taking minutes shares their screen, others in the meeting can correct what is being written. Next meeting, rotate who takes minutes. When teammates debate a specific decision, write down the essence of the argument, the output, and next steps. Ask everyone involved in the meeting if they understand what was written down, what decision was reached, and if there are lingering ambiguities about next steps. Wait seven seconds before moving on, explicitly ask people who may usually not speak up. Sometimes there is no clear decision - experimentation is needed, and that's okay. The debate can be reopened once more information is gathered - link to previous minutes to create a trail.

It doesn't have to be pretty, it just has to exist. A single place where collective understanding can be revisited is better than attempting to pass information orally.

Additionally, architecture diagrams are always helpful. Where I may have drawn on a whiteboard during a meeting to explain a mental model, I now have to take time to sketch something using a web tool like [draw.io](https://app.diagrams.net/) or [sequencediagram.org](https://sequencediagram.org/). Having some sort of picture as output of meetings really helps solidify what was discussed. These can be stored with minutes, in acceptance criteria of a work ticket, or in a shared directory of diagrams. These diagrams take longer to produce than a whiteboard and a marker, but that's okay. The act of writing these things down takes less time than orally re-explaining and rebuilding understanding.

Since my team works primarily with AWS, our team downloaded the [AWS architecture icons](https://aws.amazon.com/architecture/icons/) to quickly create diagrams. It's helpful to create a deck in something like Google Slides and make rudimentary diagrams with these icons and arrows. Proposing a new architecture can be as easy as duplicating a slide and adding new edges and nodes.

### Templates help

Any sort of design template is helpful. Save a Google Doc with headings and have your teammates create a copy when a meeting starts. Create a sample slide deck with a link to the AWS icons. Make a dummy diagram. Pin a text file in Slack with a sample sequence diagram. Any starting place, any guidance, any framework is better than reinventing every time one is needed.

### Accept slowing down

In the age of remote work, it's easy to lose our grounding in the physical realm. In _How To Do Nothing_, Jenny Odell quotes David Abram - "only in regular contact with the tangible ground and sky can we learn to orient and to navigate in the multiple dimensions that now claim us." We cannot rely on the ephemeral nature of Zoom and Slack to cement business and engineering decisions.

Recall that writers and philosophers communicated with each other by writing and mailing letters. Not email but pen-and-paper letters that occupied the physical realm. Sacasas succinctly states "writing encourages a heightened precision of expression and a sequential and systematic ordering of ideas and arguments." I'm not suggesting we mail letters, but I am suggesting we shift focus from "move fast and break things" to sit still and write down your next steps and how you've arrived at them.

Grounding ourselves in the physical act of writing meeting notes or drawing diagrams has a twofold benefit:
1. we keep ourselves centered in the non-ephemeral
2. we do others a service by better distributing information

### This blog post is meta

Even this blog is an attempt to capture my mental model on how to improve knowledge sharing and decision making at work. Taking some time to write these thoughts has helped me orient myself towards being a more effective lead. But we also have to give ourselves a break. We're experiencing an unprecedented global pandemic and it's important we give ourselves a break. Information will be lost, and most systems can afford to be a little lossy.
