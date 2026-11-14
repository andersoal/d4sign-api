// @ts-check
import { copyFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightOpenAPI, { openAPISidebarGroups } from 'starlight-openapi';
import starlightLlmsTxt from 'starlight-llms-txt';
import starlightLlmActions from 'starlight-llm-actions';

// Publishes the raw spec at /openapi.yaml so developers can import it straight into
// Postman/Insomnia/etc. without hunting through the GitHub repo.
function publishOpenApiSpec() {
	return {
		name: 'publish-openapi-spec',
		hooks: {
			'astro:build:done': ({ dir }) => {
				copyFileSync(
					fileURLToPath(new URL('../openapi/d4sign.yaml', import.meta.url)),
					fileURLToPath(new URL('./openapi.yaml', dir)),
				);
			},
		},
	};
}

// https://astro.build/config
export default defineConfig({
	site: 'https://andersoal.github.io',
	base: '/d4sign-api',
	integrations: [
		publishOpenApiSpec(),
		starlight({
			title: 'D4Sign API',
			description:
				'Unofficial, community-maintained guide and API reference for the D4Sign electronic signature API, with a PHP SDK guide and a ready-to-run Bruno collection.',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/andersoal/d4sign-api' }],
			customCss: ['./src/styles/d4sign-theme.css'],
			// English stays at the content root via the `root` locale; adding a translation later
			// is just a new `pt-br` key + a `src/content/docs/pt-br/` folder, no restructuring.
			locales: {
				root: { label: 'English', lang: 'en' },
				// 'pt-br': { label: 'Português', lang: 'pt-BR' }, // uncomment once guides are translated
			},
			editLink: {
				baseUrl: 'https://github.com/andersoal/d4sign-api/edit/master/site/',
			},
			plugins: [
				starlightOpenAPI([
					{
						base: 'reference',
						schema: '../openapi/d4sign.yaml',
						sidebar: {
							label: 'API Reference',
							collapsed: false,
							operations: { badges: true },
						},
						snippets: {
							operation: {
								clients: {
									shell: ['curl'],
									javascript: ['fetch', 'axios'],
									go: ['nethttp'],
									java: ['okhttp'],
									csharp: ['httpclient'],
								},
							},
						},
					},
				]),
				starlightLlmsTxt({ projectName: 'D4Sign API (unofficial docs)' }),
				starlightLlmActions(),
			],
			sidebar: [
				{
					label: 'Guides',
					items: [
						{ label: 'Getting Started', slug: 'guides/getting-started' },
						{ label: 'Environments', slug: 'guides/environments' },
						{ label: 'Authentication', slug: 'guides/authentication' },
						{ label: 'Core Workflows', slug: 'guides/core-workflows' },
						{ label: 'Webhooks', slug: 'guides/webhooks' },
						{ label: 'Embedding the Signing UI', slug: 'guides/embed' },
						{ label: 'Rate Limits & Errors', slug: 'guides/rate-limits-and-errors' },
					],
				},
				...openAPISidebarGroups,
				{
					label: 'Recipes',
					items: [
						{ label: 'Upload, Send, and React to Completion', slug: 'recipes/send-and-track' },
						{ label: 'Generate from a Template', slug: 'recipes/template-to-signature' },
						{ label: 'Collect a Signature via EMBED', slug: 'recipes/embed-in-your-site' },
						{ label: 'Batch + Group Signing', slug: 'recipes/batch-group-signing' },
					],
				},
				{
					label: 'PHP SDK',
					items: [{ label: 'Using the PHP SDK', slug: 'sdk/php' }],
				},
				{
					label: 'Tools',
					items: [
						{ label: 'Bruno Collection', slug: 'tools/bruno' },
						{ label: 'Raw OpenAPI Spec (YAML)', link: '/openapi.yaml', attrs: { target: '_blank' } },
					],
				},
			],
		}),
	],
});
