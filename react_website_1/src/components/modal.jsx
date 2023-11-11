// @src/components/Modal.jsx

import React from "react";
import styles from "./Modal.module.css";
import { RiCloseLine } from "react-icons/ri";


function enable(){
document.body.style.overflow = 'scroll';}


const Modal = ({ result, setIsOpen }) => {
  return (
    <>
      <div className={styles.darkBG} onClick={() => {setIsOpen(false); enable()}} />
      <div className={styles.centered}>
        <div className={styles.modal}>
          <div className={styles.modalHeader}>
            <h1 className={styles.heading}>{result.name.raw}<br/>{result.author.raw}</h1>
          </div>
          <div className="sui-result_body" style={{width: '100%' ,display:'table'}}>
            <button className={styles.closeBtn} onClick={() => {setIsOpen(false); enable()}}>
              <RiCloseLine style={{ marginBottom: "-3px" }} />
            </button>
            <div className="modal-body" style={{display:'table-row'}}>
              <div className="data" >
                <img src={result.portada.raw} alt={result.portada.raw} />
                <h5 className="modal-list">Editorial: {result.editorial.raw}</h5>
                <h5 className="modal-list">Idioma: {result.language.raw}</h5>
                <h5 className="modal-list">Páginas: {result.pages.raw}</h5>
                <h5 className="modal-list">Año: {result.year.raw}</h5>
                <h5 className="modal-list">Tags: {result.tags.raw}</h5>
              </div>
              <div style={{display:'table-cell'}} className="modal-result__details"
              dangerouslySetInnerHTML={{ __html:result.sinopsis.raw, color:'black' }}>
              </div>
            </div>
          </div>


        </div>
      </div>
    </>
  );
};

export default Modal;
