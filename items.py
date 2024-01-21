actions = {
    # triggered updates (adding a new source list)
    'update_apt_cache': {
        'cascade_skip': False,
        'command': "apt-get update",
        'triggered': True,
        'unless': "find /var/cache/apt/pkgcache.bin -mmin -60",
    },
    'force_update_apt_cache': {
        'cascade_skip': False,
        'command': "apt-get update",
        'triggered': True,
    },
    # automatic updating (new nodes / older nodes with no updates)
    'auto_update_apt_cache': {
        'command': "apt-get update",
        'needed_by': ["pkg_apt:"],
        'unless': "find /var/cache/apt/pkgcache.bin -mmin -60|grep /var/cache/apt/pkgcache.bin &> /dev/null",
    },
}

files = {
}

# move release name to debian/ ubuntu bundle
release_name = node.metadata.get(node.os, {}).get('release_name', 'jessie')

directories = {
    "/etc/apt/sources.list.d": {
        "mode": "0755",
        "owner": "root",
        "group": "root",
    },
    "/etc/apt/keyrings": {
        "mode": "0755",
        "owner": "root",
        "group": "root",
    }
}

pkg_apt = {
    'file': {},
    'apt-transport-https': {},
    'ca-certificates': {},
}

for pkg, config in node.metadata.get('apt', {}).get('packages', {}).items():
    if pkg not in pkg_apt.keys():
        # TODO: add dependency for update apt_cache
        pkg_apt[pkg] = config
        pkg_apt[pkg]['tags'] = pkg_apt[pkg].get('tags', []) + [f'pkg_{pkg}', ]

files["/etc/apt/sources.list"] = {
    "source": "sources.debian" if node.os == "debian" else "sources.ubuntu",
    "content_type": "jinja2",
    "mode": "0755",
    "owner": "root",
    "group": "root",
    'context': {
        'release_name': release_name,
        'apt_mirror': node.metadata.get('apt', {}).
            get('mirror', 'https://ftp.halifax.rwth-aachen.de/{os}'.format(os=node.os).rstrip('/'))
    },
    'triggers': ["action:force_update_apt_cache"],
    'needs': [
        'pkg_apt:apt-transport-https',
        'pkg_apt:ca-certificates',
    ],
}
