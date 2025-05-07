'use client';

import { useState, useEffect } from 'react';

interface RichTextEditorProps {
  value: string;
  onChange: (value: string) => void;
  height?: number;
  placeholder?: string;
}

export default function RichTextEditor({
  value,
  onChange,
  height = 500,
  placeholder = 'Digite seu conteúdo aqui...'
}: RichTextEditorProps) {
  const [content, setContent] = useState(value);

  // Atualizar o conteúdo quando o valor mudar
  useEffect(() => {
    setContent(value);
  }, [value]);

  // Manipular a mudança no conteúdo
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    setContent(newValue);
    onChange(newValue);
  };

  return (
    <div className="relative">
      <div className="border border-gray-300 dark:border-gray-700 rounded-md overflow-hidden">
        {/* Barra de ferramentas básica */}
        <div className="bg-gray-100 dark:bg-gray-800 p-2 border-b border-gray-300 dark:border-gray-700 flex flex-wrap gap-2">
          <button
            type="button"
            className="px-2 py-1 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-600"
            onClick={() => {
              const textarea = document.getElementById('rich-editor') as HTMLTextAreaElement;
              const start = textarea.selectionStart;
              const end = textarea.selectionEnd;
              const newText = content.substring(0, start) + '<strong>' + content.substring(start, end) + '</strong>' + content.substring(end);
              setContent(newText);
              onChange(newText);
            }}
          >
            <strong>B</strong>
          </button>
          <button
            type="button"
            className="px-2 py-1 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-600"
            onClick={() => {
              const textarea = document.getElementById('rich-editor') as HTMLTextAreaElement;
              const start = textarea.selectionStart;
              const end = textarea.selectionEnd;
              const newText = content.substring(0, start) + '<em>' + content.substring(start, end) + '</em>' + content.substring(end);
              setContent(newText);
              onChange(newText);
            }}
          >
            <em>I</em>
          </button>
          <button
            type="button"
            className="px-2 py-1 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-600"
            onClick={() => {
              const textarea = document.getElementById('rich-editor') as HTMLTextAreaElement;
              const start = textarea.selectionStart;
              const end = textarea.selectionEnd;
              const newText = content.substring(0, start) + '<h2>' + content.substring(start, end) + '</h2>' + content.substring(end);
              setContent(newText);
              onChange(newText);
            }}
          >
            H2
          </button>
          <button
            type="button"
            className="px-2 py-1 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-600"
            onClick={() => {
              const textarea = document.getElementById('rich-editor') as HTMLTextAreaElement;
              const start = textarea.selectionStart;
              const end = textarea.selectionEnd;
              const newText = content.substring(0, start) + '<p>' + content.substring(start, end) + '</p>' + content.substring(end);
              setContent(newText);
              onChange(newText);
            }}
          >
            P
          </button>
          <button
            type="button"
            className="px-2 py-1 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-600"
            onClick={() => {
              const textarea = document.getElementById('rich-editor') as HTMLTextAreaElement;
              const start = textarea.selectionStart;
              const end = textarea.selectionEnd;
              const newText = content.substring(0, start) + '<a href="#">' + content.substring(start, end) + '</a>' + content.substring(end);
              setContent(newText);
              onChange(newText);
            }}
          >
            Link
          </button>
        </div>

        {/* Área de edição */}
        <textarea
          id="rich-editor"
          value={content}
          onChange={handleChange}
          style={{ height: `${height}px` }}
          className="w-full p-4 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder={placeholder}
        />
      </div>

      {/* Visualização HTML */}
      <div className="mt-4">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Visualização HTML:</h3>
        <div
          className="p-4 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md"
          dangerouslySetInnerHTML={{ __html: content }}
        />
      </div>
    </div>
  );
}
