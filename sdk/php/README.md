# D4Sign PHP SDK

Original D4Sign PHP client. Full usage guide (with every example): [docs site → PHP SDK](https://andersoal.github.io/d4sign-api/sdk/php/).

## Install

```json
{
  "require": {
    "d4sign/d4sign-php": "dev-master"
  },
  "minimum-stability": "dev",
  "repositories": [
    { "type": "git", "url": "https://github.com/d4sign/d4sign-php" }
  ]
}
```

Requires PHP ≥ 5.5.

## Quick start

```php
require_once(__DIR__ . '/vendor/autoload.php');

use D4sign\Client;

$client = new Client();
$client->setAccessToken('{tokenAPI}');
$client->setCryptKey('{cryptKey}');

$docs = $client->documents->find();
```

See the [full guide](https://andersoal.github.io/d4sign-api/sdk/php/) for documents, signers, webhooks, and error handling, and the [API Reference](https://andersoal.github.io/d4sign-api/reference/) for anything this SDK doesn't cover.
