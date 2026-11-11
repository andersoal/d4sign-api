// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightOpenAPI from 'starlight-openapi';
import starlightLlmsTxt from 'starlight-llms-txt';

// https://astro.build/config
export default defineConfig({
	site: 'https://andersoal.github.io',
	base: '/d4sign-api',
	integrations: [
		starlight({
			title: 'D4Sign API',
			description:
				'Unofficial, community-maintained guide and API reference for the D4Sign electronic signature API, with a PHP SDK guide and a ready-to-run Bruno collection.',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/andersoal/d4sign-api' }],
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
						sidebar: { label: 'API Reference', collapsed: false },
					},
				]),
				starlightLlmsTxt({ projectName: 'D4Sign API (unofficial docs)' }),
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
					items: [{ label: 'Bruno Collection', slug: 'tools/bruno' }],
				},
			],
		}),
	],
});
