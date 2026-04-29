// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'nautil',
			favicon: './favicon.ico',
			logo: {
				dark: './src/assets/logo500.png',
				light: './src/assets/logo500.png',
				replacesTitle: false,
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/neylz/nautil' },
				{ icon: 'discord', label: 'Discord', href: 'https://discord.gg/Psk3mxEnjj' },
			],
			sidebar: [
				{
					label: 'Start Here',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Installation', slug: 'guide/install' },
						{ label: 'Getting Started', slug: 'guide/get-started' },
						{ label: 'Using Artifacts', slug: 'guide/using-artifacts' },
						{ label: 'Using Sources', slug: 'guide/using-sources' },
						{ label: 'Custom Action', slug: 'guide/custom-action' },
						{ label: 'Custom Plugin', slug: 'guide/custom-plugin' },
					],
				},
				{
					label: 'Plugins',
					autogenerate: { directory: 'plugin', collapsed: true },
				},
			],
			customCss: [
				'./src/fonts/font-face.css',
				'./src/styles/custom.css',
			],
		}),
	],
});
