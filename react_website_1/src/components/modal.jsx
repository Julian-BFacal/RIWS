// @src/components/Modal.jsx

import React from "react";
import styles from "./Modal.module.css";
import { RiCloseLine } from "react-icons/ri";

const Modal = ({ result, setIsOpen }) => {
  return (
    <>
      <div className={styles.darkBG} onClick={() => setIsOpen(false)} />
      <div className={styles.centered}>
        <div className={styles.modal}>
          <div className={styles.modalHeader}>
            <h1 className={styles.heading}>{result.name.raw}</h1>
          </div>
          <div className="sui-result_body" style={{width: '100%' ,display:'table'}}>
            <div style={{display:'table-row'}}>
              <div className="data" style={{width: '25%', display:'table-cell', padding: '50px'}}>
                <img src={result.portada.raw} alt={result.portada.raw} />
                <h5 style={{color:'black'}}>Tags: {result.tags.raw}</h5>
                <h5 style={{color:'black'}}>Editorial: {result.editorial.raw}</h5>
                <h5 style={{color:'black'}}>Idioma: {result.language.raw}</h5>
                <h5 style={{color:'black'}}>Páginas: {result.pages.raw}</h5>
                <h5 style={{color:'black'}}>Año: {result.year.raw}</h5>
              </div>
              <div style={{display:'table-cell'}} className="sui-result__details"
              dangerouslySetInnerHTML={{ __html: result.sinopsis.raw, color:'black' }}>
              </div>
            </div>
          </div>


        </div>
      </div>
    </>
  );
};

export default Modal;
