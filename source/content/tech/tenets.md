Title: Tenets
Date: 2020-07-23 15:00
Category: tech
Tags: tech
Slug: tenets
Authors: james
Summary: Test in prod
Status: draft

I lead a team of a few engineers working to provide observability tooling for a handful of other teams all operating serverless functions and services to handle asynchronous workloads. While the serverless model gives us some nice isolation when it comes to supporting multiple tenants of a platform, it provides some challenge when instrumenting observability. I think we're in early days of providing performant tooling for serverless environments.

It's an exciting product and I've been introducing myself to lots folks as the client project and [consulting firm](https://nuvalence.io) has been growing rapidly. After so many introductions and leading a team for six months, stepping back I've distilled my work philosophy into two major tenets.

1. Focus on production, everything else is [vaporware](https://en.wikipedia.org/wiki/Vaporware).

Your development environment doesn't matter. Your staging environment doesn't matter. Your end to end tests running in anything but production don't tell you anything. Production traffic is the only thing that matters. Systems and flows that enable your business to serve your customers matter. Charity Majors has some great thoughts on the [critical path](https://charity.wtf/2020/07/24/questionable-advice-whats-the-critical-path/). Know what it is for you and your team and focus on operating that path.

If your team provides internal tooling or "foundational services," find and track how other teams are using your stuff in production. Find out if and where your services are used in the critical path in _production_.

2. Minimize operational burden so everyone can sleep.
