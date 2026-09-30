# ASPHAM

American Society for the Philosophy of Aesthetic Medicine.

This repository delivers the 48-page public reader website to Linevast. It includes the original ASPHAM identity, guided reading paths, source profiles, and the historical foundations Aesthetica 1750 and Medical Ethics 1803. These years refer to the historical works.

Target website: https://aspham.org/

## Deployment

The release archive contains public HTML, React hydration assets, supplied brand assets, a route list, and a SHA-256 file manifest. SHA256SUMS verifies the archive. The cPanel deployment task runs install-linevast.py, verifies every file, saves the previous website, and installs only in the confirmed ASPHAM document root.

The canonical editable application remains in the local ASPHAM workspace. This package publishes reader content; private administration, reporting, booking, payments, D1/R2, and certification processing are outside this deployment. The empty register reflects the checked release state.

Installation and public HTTPS checks are separate steps. See the deployment receipt for the observed result.

The supplied ASPHAM brand assets remain subject to their owner's rights. This repository grants no additional license.
