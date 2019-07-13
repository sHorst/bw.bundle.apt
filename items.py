actions = {
    # triggered updates (adding a new source list)
    'update_apt_cache': {
        'cascade_skip': False,
        'command': "apt-get update",
        'triggered': True,
        'unless': "find /var/cache/apt/pkgcache.bin -mmin -60",
    },
    # automatic updating (new nodes / older nodes with no updates)
    'auto_update_apt_cache': {
        'command': "apt-get update",
        'needed_by': ["pkg_apt:"],
        'unless': "find /var/cache/apt/pkgcache.bin -mmin -60|grep /var/cache/apt/pkgcache.bin",
    },
}

files = {
}

release_names = {
    'debian': {
        8: 'jessie',
        9: 'stretch',
        10: 'buster',
        11: 'bullseye',
        12: 'bookworm',
    }
}

release_name = release_names.get(node.os, {}).get(node.os_version[0], 'jessie')

directories = {
    "/etc/apt/sources.list.d": {
        "mode": "0755",
        "owner": "root",
        "group": "root",
    },
}

pkg_apt = {
    'file': {},
    'apt-transport-https': {},
}

for pkg, config in node.metadata.get('apt', {}).get('packages', {}).items():
    if pkg not in pkg_apt.keys():
        # TODO: add dependency for update apt_cache
        pkg_apt[pkg] = config

files["/etc/apt/sources.list"] = {
    "source": "sources.list",
    "content_type": "jinja2",
    "mode": "0755",
    "owner": "root",
    "group": "root",
    'context': {
        'release_name': release_name,
        'apt_mirror': node.metadata.get('apt', {}).get('mirror', 'http://ftp.halifax.rwth-aachen.de/debian/')
    },
    'triggers': ["action:update_apt_cache"],
}
