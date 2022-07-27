# Change Log


## [0.1.0] - Initial Release

The first release which supports:

- Application Button
- Quick Access Buttons
- Category
- Panel
- Gallery
- And so on ...

## [0.1.1-0.1.2] Fixed some bugs

- Fixed bugs of not finding icons/styles files

## [0.1.3] Fixed some bugs

- Fixed bugs: font of popup gallery is not consistent with main window 
  ([fe7df17](https://github.com/haiiliin/pyqtribbon/commit/fe7df170c520234e172fd03d39b2e81b5b01b991)).
- Add support to customize the panel options 
  ([f061618](https://github.com/haiiliin/pyqtribbon/commit/f061618f879c64ef55dfcc831a59093c8fd3f4c8)).
- Fix setRibbonStyle() bug: not handle the debug style correctly
  ([e218162](https://github.com/haiiliin/pyqtribbon/commit/e2181626d92639834d8a80f8da2f95dc4e6cdb46)).

## [0.1.4] Rename classes to Ribbon-like

- Rename CategoryStyle to RibbonCategoryStyle
  ([c243f50](https://github.com/haiiliin/pyqtribbon/commit/c243f508311271c6309b5c0c4d0f899668e36b6d)).
- Rename ButtonStyle to RibbonButtonStyle
  ([c7efad1](https://github.com/haiiliin/pyqtribbon/commit/c7efad1c5a5c43f50ba8deeff57dd53c5b1c17e5)).
- Rename SpaceFindMode to RibbonSpaceFindMode, GridLayoutManager to RibbonGridLayoutManager 
  ([6c8e8bc](https://github.com/haiiliin/pyqtribbon/commit/6c8e8bcb10a412a430a9f481380c12a73b6c9984)).

## [0.1.5] Update RibbonMainWindows and Add Tutorials

- Update RibbonMainWindow 
  ([a39cf03](https://github.com/haiiliin/pyqtribbon/commit/a39cf033fe3e57e941c00f76038761c4d71dd80f)).
- Add tutorials docs
  ([a8f8f83](https://github.com/haiiliin/pyqtribbon/commit/a8f8f836a200cac3028481d6f046fad3cf1776dd)).
  
## [0.1.6] Show inheritance class and add overloaded constructors

- Show inheritance class 
  ([1e06989](https://github.com/haiiliin/pyqtribbon/commit/1e06989b57813840e04b2f8f69788c3ee6026274)).
- Add overloaded methods to be compatible with QWidget
  ([0886675](https://github.com/haiiliin/pyqtribbon/commit/0886675b2da7d5aacb757a4e955b71e49cc20f1b)).

## [0.1.7] Update docs

- Add RibbonBar.helpRibbonButton method
  ([31239b0](https://github.com/haiiliin/pyqtribbon/commit/31239b0b557cc0a91d450be1a7614b518eed02d6)).
- Add User Manual
  ([b1c7b37](https://github.com/haiiliin/pyqtribbon/commit/b1c7b37c6e4b11e6b8a5492bf94c4955c16cf2ba)).
## [0.1.8] Add tests for multiple Python versions

- Add tests to support multiple Python versions
  ([a4d9282](https://github.com/haiiliin/pyqtribbon/commit/a4d9282da76bee0a3e625d8f266380d1d8b9a704), 
  [ee7e845](https://github.com/haiiliin/pyqtribbon/commit/ee7e8453f0991b24c163305c388d6da28a2b1747)).

## [0.1.9] Fixed bugs of compatibilities  for different Qt versions

- sphinx_qt_documentation
  ([a18a9fa](https://github.com/haiiliin/pyqtribbon/commit/a18a9fac21445e8adfdcca82036254b3277304c8)).
- Use qtpy to be compatiable with different Qt versions
  ([0d45931](https://github.com/haiiliin/pyqtribbon/commit/0d4593159f5ba8e1b8787419f5bd6520ed035582)).
- Use QApplication.instance() instead of qApp to be compatible with PyQt6
  ([75d3953](https://github.com/haiiliin/pyqtribbon/commit/75d395328541ccea829e2e33012ea4c1cba74628)).

## [0.1.10] Update docs

- Add type hints for returns
  ([b1ef8f1](https://github.com/haiiliin/pyqtribbon/commit/b1ef8f10377e619634108ce6400897070f40fc55), 
  [4422772](https://github.com/haiiliin/pyqtribbon/commit/44227722280373a1af89571a8003cc121a4efa70)).

## [0.1.11] Update ribbon.catogories, category.panels, and panel.titleText

- Update catogories to a dict, add panels method
  ([679c04d](https://github.com/haiiliin/pyqtribbon/commit/679c04d04adfe8fe92443fb34b6ac2ed00d40355)).
- Rename titleText to title
  ([3e48852](https://github.com/haiiliin/pyqtribbon/commit/3e48852cf71e543eda8813b7e8cafdc6bbfcaa84)).

## [0.1.12] Update examples and tutorials, Update base class of RibbonBar and remove RibbonMainWindow

- Update examples and tutorials 
  ([a37dcdf](https://github.com/haiiliin/pyqtribbon/commit/a37dcdfa8d4eae74bfb6a1186fb63914d35a5c42),
  [f9a6b55](https://github.com/haiiliin/pyqtribbon/commit/f9a6b55d9da7b17838ff72021f48e7af1a5941d7)).
- Add alignment for addGallery 
  ([ba6458d](https://github.com/haiiliin/pyqtribbon/commit/ba6458d49d94bc85dc8b8a1434641e58d103c84b)).
- Update base class of RibbonBar
  ([7bc81bb](https://github.com/haiiliin/pyqtribbon/commit/7bc81bbaf3d8bba5ed3309f5424e353185d1df9e)).
- Remove RibbonMainWindow 
  ([c47bd6f](https://github.com/haiiliin/pyqtribbon/commit/c47bd6fc797431e7effc7898a53c7039a7bc9356)). 

## The change log will now be displayed in the release page.
