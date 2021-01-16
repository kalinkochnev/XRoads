import { faBold, faItalic, faListOl, faListUl, faQuoteLeft, faUnderline } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { convertFromRaw, convertToRaw, Editor, EditorState, getDefaultKeyBinding, RichUtils } from 'draft-js';
import 'draft-js/dist/Draft.css';
import { draftToMarkdown, markdownToDraft } from 'markdown-draft-js';
import React from 'react';
import './RichEditor.scss';
const { useState, useRef, useCallback } = React;

function RichEditor({ initialValue, setValue = (value) => null }) {
  const currContentState = convertFromRaw(markdownToDraft(initialValue));
  const [editorState, setEditorState] = useState(EditorState.createWithContent(currContentState));

  const editor = useRef(null);

  const focus = () => {
    if (editor.current) editor.current.focus();
  };

  const handleKeyCommand = useCallback(
    (command, editorState) => {
      const newState = RichUtils.handleKeyCommand(editorState, command);
      if (newState) {
        setEditorState(newState);
        return 'handled';
      }
      return 'not-handled';
    },
    [editorState, setEditorState],
  );

  const mapKeyToEditorCommand = useCallback(
    e => {
      switch (e.keyCode) {
        case 9: // TAB
          const newEditorState = RichUtils.onTab(
            e,
            editorState,
            4 /* maxDepth */,
          );
          if (newEditorState !== editorState) {
            setEditorState(newEditorState);
          }
          return null;
      }
      return getDefaultKeyBinding(e);
    },
    [editorState, setEditorState],
  );

  // If the user changes block type before entering any text, we can
  // either style the placeholder or hide it. Let's just hide it now.
  let className = 'RichEditor-editor';
  var contentState = editorState.getCurrentContent();
  if (!contentState.hasText()) {
    if (
      contentState
        .getBlockMap()
        .first()
        .getType() !== 'unstyled'
    ) {
      className += ' RichEditor-hidePlaceholder';
    }
  }

  const updateEditorState = (newEditorState) => {
    const content = newEditorState.getCurrentContent();
    const rawObject = convertToRaw(content);
    const markdownString = draftToMarkdown(rawObject);
    setValue(markdownString);
    setEditorState(newEditorState);
  }

  return (
    <div className="RichEditor-root">
      <InlineStyleControls
        editorState={editorState}
        onToggle={inlineStyle => {
          const newState = RichUtils.toggleInlineStyle(
            editorState,
            inlineStyle,
          );
          setEditorState(newState);
        }}
      />
      <BlockStyleControls
        editorState={editorState}
        onToggle={blockType => {
          const newState = RichUtils.toggleBlockType(editorState, blockType);
          setEditorState(newState);
        }}
      />
      <div className={className} onClick={focus}>
        <Editor
          blockStyleFn={getBlockStyle}
          customStyleMap={styleMap}
          editorState={editorState}
          handleKeyCommand={handleKeyCommand}
          keyBindingFn={mapKeyToEditorCommand}
          onChange={updateEditorState}
          ref={editor}
          spellCheck={true}
        />
      </div>
    </div>
  );
}

// Custom overrides for "code" style.
const styleMap = {
  CODE: {
    backgroundColor: 'rgba(0, 0, 0, 0.05)',
    fontFamily: '"Inconsolata", "Menlo", "Consolas", monospace',
    fontSize: 16,
    padding: 2,
  },
};

function getBlockStyle(block) {
  switch (block.getType()) {
    case 'blockquote':
      return 'RichEditor-blockquote';
    default:
      return null;
  }
}

function StyleButton({ onToggle, active, label, icon, style }) {
  let className = 'RichEditor-styleButton';
  if (active) {
    className += ' RichEditor-activeButton';
  }

  return (
    <span
      className={className}
      onMouseDown={e => {
        e.preventDefault();
        onToggle(style);
      }}>
      {typeof (label) == 'string' && <b>{label}</b>}
      { icon && <FontAwesomeIcon icon={icon} />}

    </span>
  );
}

const BLOCK_TYPES = [
  { id: 'h1', label: 'H1', style: 'header-one' },
  { id: 'h2', label: 'H2', style: 'header-two' },
  { id: 'h3', label: 'H3', style: 'header-three' },
  { id: 'leftQuote', icon: faQuoteLeft, style: 'blockquote' },
  { id: 'unorderedList', icon: faListUl, style: 'unordered-list-item' },
  { id: 'orderedList', icon: faListOl, style: 'ordered-list-item' },
];

function BlockStyleControls({ editorState, onToggle }) {
  const selection = editorState.getSelection();
  const blockType = editorState
    .getCurrentContent()
    .getBlockForKey(selection.getStartKey())
    .getType();

  return (
    <div className="RichEditor-controls RichEditor-blockControls">
      {BLOCK_TYPES.map(type => (
        <StyleButton
          key={type.id}
          active={type.style === blockType}
          label={type.label}
          onToggle={onToggle}
          style={type.style}
          icon={type.icon}
        />
      ))}
    </div>
  );
}

const INLINE_STYLES = [
  { id: 'bold', label: faBold, icon: faBold, style: 'BOLD' },
  { id: 'italic', label: faItalic, icon: faItalic, style: 'ITALIC' },
  { id: 'underline', label: faUnderline, icon: faUnderline, style: 'UNDERLINE' },
];

function InlineStyleControls({ editorState, onToggle }) {
  const currentStyle = editorState.getCurrentInlineStyle();
  return (
    <div className="RichEditor-controls">
      {INLINE_STYLES.map(type => (
        <StyleButton
          key={type.id}
          active={currentStyle.has(type.style)}
          label={type.label}
          onToggle={onToggle}
          style={type.style}
          icon={type.icon}
        />
      ))}
    </div>
  );
}

export default RichEditor;