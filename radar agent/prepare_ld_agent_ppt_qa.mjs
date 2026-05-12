import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';

const root = 'D:/knowledge/radar agent';
const deckPath = `${root}/LD智能体科研报告PPT/index.html`;
const qaDir = `${root}/LD智能体科研报告PPT/qa`;
mkdirSync(qaDir, { recursive: true });

const html = readFileSync(deckPath, 'utf8');
const slides = [1, 4, 7, 9, 13];

for (const slide of slides) {
  const presses = slide - 1;
  const injected = `
<script>
window.addEventListener('load', () => {
  setTimeout(() => {
    for (let i = 0; i < ${presses}; i += 1) {
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight' }));
    }
  }, 500);
});
</script>
`;
  const out = html.replace('</body>', `${injected}</body>`);
  writeFileSync(`${qaDir}/slide-${String(slide).padStart(2, '0')}.html`, out, 'utf8');
}

console.log(JSON.stringify({ qaDir, slides }, null, 2));
