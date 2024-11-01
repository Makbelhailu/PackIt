import React from "react";
import Packager from "../../components/Packagers/Packager";
import Header from "../../components/Header/Header";
import Footer from "../../components/Footer/Footer";

const PackagePage = ({ cartItems, allProductsData, addToCart }) => {
    return (
        <>
            <Header cartItems={cartItems} />
            <Packager
                allProductsData={allProductsData}
                addToCart={addToCart}
            />
            <Footer />
        </>
    );
};

export default PackagePage;
