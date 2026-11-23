# RADIO Lab Archive

A GitHub Pages archive for RADIO lab reports and prelabs. PDFs are indexed automatically by folder.

## Publish the site

1. Create a GitHub repository named `radio-lab-archive` (or choose your own name). On GitHub Free, use a public repository for Pages.
2. Extract the ZIP. Commit and push its contents, including the hidden `.github/` directory, to the repository's `main` branch. Keep `build.py` at the repository root.
3. In the repository, go to **Settings → Pages**. Under **Build and deployment**, select **GitHub Actions** as the source.
4. In **Actions → Publish RADIO archive**, choose **Run workflow** on `main`. When the deployment succeeds, find the site URL in **Settings → Pages**.

## Add or remove PDFs

| Document | Folder |
| --- | --- |
| Prelab | `reports/prelabs/` |
| Lab report | `reports/lab-reports/` |

On GitHub, open the appropriate folder and use **Add file → Upload files**. Give each PDF a descriptive filename such as `Lab 02 - Near-field Measurements.pdf`. Commit the change to `main` to rebuild and deploy the site. To remove a PDF, delete it from its folder and commit the change.

The site uses filenames as document titles and handles spaces and Unicode. Put PDFs directly in their folder. The Pages deployment and the files included in it are public on a standard GitHub Pages site.

## Preview locally

From the project directory, run the following commands and open [localhost:8000](http://localhost:8000).

```sh
python3 build.py
python3 -m http.server 8000 --directory _site
```
