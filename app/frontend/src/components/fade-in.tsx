import React, { useState, useEffect } from 'react';

interface FadeInProps {
    children: React.ReactNode;
    isLoading: boolean;
    loader: React.ReactNode;
}

const FadeIn: React.FC<FadeInProps> = ({ children, isLoading, loader }) => {
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        if (!isLoading) {
            setIsLoaded(true);
        }
    }, [isLoading]);

    if (isLoading) {
        return <>{loader}</>;
    }

    return (
        <div className={isLoaded ? 'fade-in' : ''}>
            {children}
        </div>
    );
};

export default FadeIn;
