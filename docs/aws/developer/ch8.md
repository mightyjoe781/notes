## CI/CD

### Continous Integration

- CI is a practice, supported by people and software
- continously integrating small changes to code into existing codebase using git, build automation, linters etc.

Creating a development Environment

- local development environment mirrors production code
- `vagrant` + `virtualbox` : to create VMs

NOTE : we could something liike puppet or ansible playbook also in place of vagrant

Some important vagrant commands :

````
vagrant up
vagrant ssh
vagrant halt
vagrant destroy
````

<hr>

### Version Control System (VCS)

- Tracking changes to code overtime
- Git Basics are required to achieve this
  - Personal Notes
  - Blog Article Link

<hr>

### Testing

- All code should be considered broken until proven otherwise
- Unit Testing and Integration Testing

- Testing is important because it catches problems early when they are cheap to fix

````
Unit Testing -----------------------------> Integration Testing
|																									 ^
|-----> Linters ---> Coverage ---> Static Scans ---|
````

<hr>

### Database Schema Changes

- Schema Migration poses Challenges
- ORM + Schema Migration tools + Strategy could easily help in tracking DB Changes
- ORM stands for Object Relation Mapper

Some good DB practices

- Database should be versioned
- One Schems Change per migration
- Changes should be non-destructive
- New columns require same defaults

<hr>

### CI with Jenkins