import React, { useEffect, useState } from 'react';
import { codeToHtml } from 'shiki';

/**
 * Componente CodeBlock para resaltar sintaxis de código usando Shiki.
 * Props:
 *   - code: string (código fuente a mostrar)
 *   - language: string (lenguaje, ej: 'js', 'python')
 *   - theme: string (tema de Shiki, ej: 'nord', 'github-dark')
 *   - ...props: otros props para el div contenedor
 *
 * Ejemplo de uso:
 * <CodeBlock code={"console.log('Hola')"} language="js" theme="nord" />
 */
export default function CodeBlock({ code, language = 'js', theme = 'nord', ...props }) {
  const [codeHtml, setCodeHtml] = useState('');

  useEffect(() => {
    async function highlight() {
      const result = await codeToHtml(code, { lang: language, theme });
      setCodeHtml(result);
    }
    highlight();
  }, [code, language, theme]);

  return (
    <div
      dangerouslySetInnerHTML={{ __html: codeHtml }}
      {...props}
    />
  );
} 