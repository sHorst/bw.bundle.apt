# Bundle for apt
Set Mirror, and some other useful stuff.

## Config Values
### mirror
- Default: http://ftp.halifax.rwth-aachen.de/debian/

### security
Enable ``http://security.debian.org/debian-security {{release_name}}`` repository
- Default: True

### updates
Enable ``mirror  {{ release_name }}-updates`` repo
- Default: True

### backports
Enable ``mirror {{ release_name }}-backports`` repo
- Default: False

### packages
Do stuff with packages, via apt
- Values: ```{'packageName': {config}}```
- Default: {}