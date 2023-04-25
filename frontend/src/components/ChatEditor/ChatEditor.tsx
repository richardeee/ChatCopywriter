import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

interface ChatEditorProperties {
  data: string;
  onChange: (newData: string) => void;
}
const modules = {
  toolbar: [
    [{ 'header': [1, 2, false] }],
    ['bold', 'italic', 'underline','strike', 'blockquote'],
    [{'list': 'ordered'}, {'list': 'bullet'}, {'indent': '-1'}, {'indent': '+1'}],
    ['link', 'image'],
    ['clean']
  ],
}

const formats = [
  'header',
  'bold', 'italic', 'underline', 'strike', 'blockquote',
  'list', 'bullet', 'indent',
  'link', 'image'
]

export const ChatEditor = ({ data, onChange }: ChatEditorProperties) => {
  return (
    <div className="w-full h-full border p-1">
      <ReactQuill value={data} onChange={onChange} theme="snow" modules={modules} formats={formats}/>
    </div>
  );
};