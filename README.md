New post:
```
cd _docs/
hugo new posts/post_name.md
```

For development:
```
cd _docs/
hugo server -D
```

To build:
```
cd _docs/
hugo
```
then move everything inside `_docs/public/` to repo root.

In case the submodules is no longer available, replace the `themes` in the `_docs` with `themes_backup`.
